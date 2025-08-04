echo "echo \"Hello World\"

echo \"New Lines\"" > temp.sh
touch abc.c xyz.py mno.go

echo "#include<stdio.h>
int main(){
printf(\"Hello World\");
}"  > abc.c

echo "print(\'Hello World\')" > xyz.py

echo "package main

import \"fmt\"

func main(){
fmt.Print(\"Hello World\")
}" > mno.go

file abc.*
file xyz.*
file mno.*

cat temp.sh
head temp.sh
tail temp.sh
mkdir toDelete
cp temp.sh ./toDelete
cd toDelete
rm temp.sh
cd ..
mv temp.sh ./toDelete
mv ./toDelete/temp.sh ./
rm -r toDelete

which cat
which ls
whereis nano
locate *
find . -name *.sh

