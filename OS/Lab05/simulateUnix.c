#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <dirent.h>
#include <pwd.h>
#include <grp.h>
#include <time.h>
#include <fcntl.h>

void ls_command(const char *path) {
    DIR *dir;
    struct dirent *entry;
    struct stat file_stat;
    struct passwd *pw;
    struct group *gr;
    char full_path[1024];
    char permissions[11];
    char time_str[100];    
    if (path == NULL) {
        path = ".";
    }    
    dir = opendir(path);
    if (dir == NULL) {
        perror("Error opening directory");
        return;
    }    
    printf("total files in directory:\n");    
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_name[0] == '.' && strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
            continue;
        }        
        snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name);        
        if (stat(full_path, &file_stat) == -1) {
            perror("stat");
            continue;
        }
        permissions[0] = S_ISDIR(file_stat.st_mode) ? 'd' : '-';
        permissions[1] = (file_stat.st_mode & S_IRUSR) ? 'r' : '-';
        permissions[2] = (file_stat.st_mode & S_IWUSR) ? 'w' : '-';
        permissions[3] = (file_stat.st_mode & S_IXUSR) ? 'x' : '-';
        permissions[4] = (file_stat.st_mode & S_IRGRP) ? 'r' : '-';
        permissions[5] = (file_stat.st_mode & S_IWGRP) ? 'w' : '-';
        permissions[6] = (file_stat.st_mode & S_IXGRP) ? 'x' : '-';
        permissions[7] = (file_stat.st_mode & S_IROTH) ? 'r' : '-';
        permissions[8] = (file_stat.st_mode & S_IWOTH) ? 'w' : '-';
        permissions[9] = (file_stat.st_mode & S_IXOTH) ? 'x' : '-';
        permissions[10] = '\0';        
        pw = getpwuid(file_stat.st_uid);
        gr = getgrgid(file_stat.st_gid);
        strftime(time_str, sizeof(time_str), "%b %d %H:%M", localtime(&file_stat.st_mtime));        
        printf("%s %3ld %s %s %8ld %s %s\n",
               permissions,
               file_stat.st_nlink,
               pw ? pw->pw_name : "unknown",
               gr ? gr->gr_name : "unknown",
               file_stat.st_size,
               time_str,
               entry->d_name);
    }    
    closedir(dir);
}

void cp_command(const char *source, const char *destination) {
    FILE *src, *dest;
    char buffer[4096];
    size_t bytes_read;    
    src = fopen(source, "rb");
    if (src == NULL) {
        perror("Error opening source file");
        return;
    }    
    dest = fopen(destination, "wb");
    if (dest == NULL) {
        perror("Error opening destination file");
        fclose(src);
        return;
    }    
    while ((bytes_read = fread(buffer, 1, sizeof(buffer), src)) > 0) {
        if (fwrite(buffer, 1, bytes_read, dest) != bytes_read) {
            perror("Error writing to destination file");
            break;
        }
    }    
    fclose(src);
    fclose(dest);
    printf("File copied successfully from %s to %s\n", source, destination);
}

void wc_command(const char *filename) {
    FILE *file;
    int lines = 0, words = 0, chars = 0;
    char ch, prev_ch = ' ';    
    file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        return;
    }    
    while ((ch = fgetc(file)) != EOF) {
        chars++;        
        if (ch == '\n') {
            lines++;
        }
        if ((prev_ch == ' ' || prev_ch == '\t' || prev_ch == '\n') && 
            (ch != ' ' && ch != '\t' && ch != '\n')) {
            words++;
        }
        
        prev_ch = ch;
    }
    if (chars > 0 && prev_ch != '\n') {
        lines++;
    }    
    fclose(file);
    printf(" %d  %d %d %s\n", lines, words, chars, filename);
}

int main() {
    int choice;
    char source[256], destination[256], filename[256], directory[256];    
    while (1) {
        printf("\n=== Unix Command Simulator ===\n");
        printf("1. ls -l (list directory contents)\n");
        printf("2. cp (copy file)\n");
        printf("3. wc (word count)\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);        
        switch (choice) {
            case 1:
                printf("Enter directory path (or press Enter for current directory): ");
                getchar();
                fgets(directory, sizeof(directory), stdin);
                directory[strcspn(directory, "\n")] = 0;                
                if (strlen(directory) == 0) {
                    ls_command(".");
                } else {
                    ls_command(directory);
                }
                break;                
            case 2:
                printf("Enter source file: ");
                scanf("%s", source);
                printf("Enter destination file: ");
                scanf("%s", destination);
                cp_command(source, destination);
                break;                
            case 3:
                printf("Enter filename: ");
                scanf("%s", filename);
                wc_command(filename);
                break;                
            case 4:
                printf("Exiting...\n");
                exit(0);                
            default:
                printf("Invalid choice! Please try again.\n");
        }
    }
    return EXIT_SUCCESS;
}
