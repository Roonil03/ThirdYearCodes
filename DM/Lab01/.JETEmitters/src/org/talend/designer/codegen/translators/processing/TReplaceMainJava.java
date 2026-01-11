package org.talend.designer.codegen.translators.processing;

import org.talend.core.model.process.INode;
import org.talend.core.model.metadata.IMetadataTable;
import org.talend.core.model.metadata.IMetadataColumn;
import org.talend.core.model.process.ElementParameterParser;
import org.talend.core.model.process.IConnection;
import org.talend.designer.codegen.config.CodeGeneratorArgument;
import java.util.List;
import java.util.Map;
import org.talend.core.model.process.IConnectionCategory;

public class TReplaceMainJava
{
  protected static String nl;
  public static synchronized TReplaceMainJava create(String lineSeparator)
  {
    nl = lineSeparator;
    TReplaceMainJava result = new TReplaceMainJava();
    nl = null;
    return result;
  }

  public final String NL = nl == null ? (System.getProperties().getProperty("line.separator")) : nl;
  protected final String TEXT_1 = "";
  protected final String TEXT_2 = NL + "\t\t\t\t\t\tString searchStr_";
  protected final String TEXT_3 = "_";
  protected final String TEXT_4 = " = ";
  protected final String TEXT_5 = ";";
  protected final String TEXT_6 = " + \"\";";
  protected final String TEXT_7 = NL + "                    \tsearchStr_";
  protected final String TEXT_8 = " = org.apache.oro.text.GlobCompiler.globToPerl5(searchStr_";
  protected final String TEXT_9 = ".toCharArray(), org.apache.oro.text.GlobCompiler.DEFAULT_MASK);";
  protected final String TEXT_10 = NL + "                    \t\tsearchStr_";
  protected final String TEXT_11 = " = \"^\" + searchStr_";
  protected final String TEXT_12 = " + \"$\";";
  protected final String TEXT_13 = " = \"(?i)\" + searchStr_";
  protected final String TEXT_14 = NL + "\t                \t\t";
  protected final String TEXT_15 = ".";
  protected final String TEXT_16 = " = StringUtils.replaceAll(";
  protected final String TEXT_17 = ", searchStr_";
  protected final String TEXT_18 = ", ";
  protected final String TEXT_19 = ");";
  protected final String TEXT_20 = NL + "\t\t                    ";
  protected final String TEXT_21 = " + \"\");";
  protected final String TEXT_22 = NL + "\t              \t\t\t";
  protected final String TEXT_23 = " = StringUtils.replaceAllStrictly(";
  protected final String TEXT_24 = NL + "\t\t\t\t\t\t\t";
  protected final String TEXT_25 = " + \"\", ";
  protected final String TEXT_26 = NL + "\t\t\t\t\t";
  protected final String TEXT_27 = ");" + NL + "\t\t\t\t\t";
  protected final String TEXT_28 = NL + "                    ";
  protected final String TEXT_29 = "                ";
  protected final String TEXT_30 = NL + "\t        ";
  protected final String TEXT_31 = ";" + NL + "\t        ";
  protected final String TEXT_32 = NL + "    nb_line_";
  protected final String TEXT_33 = "++;";
  protected final String TEXT_34 = NL;

  public String generate(Object argument)
  {
    final StringBuffer stringBuffer = new StringBuffer();
    stringBuffer.append(TEXT_1);
    
CodeGeneratorArgument codeGenArgument = (CodeGeneratorArgument) argument;
INode node = (INode)codeGenArgument.getArgument();
String cid = node.getUniqueName();
boolean strictMatch = ("true").equals(ElementParameterParser.getValue( node, "__STRICT_MATCH__" ));
String incomingConnName = null;
List<? extends IConnection> inConns = node.getIncomingConnections();
if(inConns != null && inConns.size() > 0) {
    IConnection inConn = inConns.get(0);
    incomingConnName = inConn.getName();
}
List<IMetadataColumn> columnList = null;
List<IMetadataTable> metadataTables = node.getMetadataList();
if(metadataTables != null && metadataTables.size() > 0) {
    IMetadataTable metadataTable = metadataTables.get(0);
    columnList = metadataTable.getListColumns();
}
List<? extends IConnection> outgoingConns = node.getOutgoingSortedConnections();


if(incomingConnName != null && columnList != null && columnList.size() > 0) {
    String advancedMode = ElementParameterParser.getValue( node, "__ADVANCED_MODE__" );
    String simpleMode = ElementParameterParser.getValue( node, "__SIMPLE_MODE__" );
    
    List<Map<String, String>> patterns = null;
          
    //simple mode Replacement    
    if(("true").equals(simpleMode)) {
        List<Map<String, String>> substitutions = (List<Map<String,String>>)ElementParameterParser.getObjectValue(node,"__SUBSTITUTIONS__");
        if(substitutions != null && substitutions.size() > 0) {
        	int i = 0;
            for(Map<String,String> substitution : substitutions) {            	
                String replaceStr = substitution.get("REPLACE_STRING");
                if(replaceStr != null && !("").equals(replaceStr)) {                	
                    String searchStr = substitution.get("SEARCH_PATTERN");
                    i++;
                    if(("null").equals(searchStr.toLowerCase())){

    stringBuffer.append(TEXT_2);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_4);
    stringBuffer.append(searchStr );
    stringBuffer.append(TEXT_5);
    
					}else{

    stringBuffer.append(TEXT_2);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_4);
    stringBuffer.append(searchStr );
    stringBuffer.append(TEXT_6);
    
					}
					if(("true").equals(substitution.get("USE_GLOB"))){

    stringBuffer.append(TEXT_7);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_8);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_9);
    
					}
					//this component only support strict match from now on (Bug 10232).
					//for old behaviour support
                	if(!strictMatch){
						if(("true").equals(substitution.get("WHOLE_WORD"))){

    stringBuffer.append(TEXT_10);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_11);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_12);
    						}
						if(("false").equals(substitution.get("CASE_SENSITIVE"))){

    stringBuffer.append(TEXT_10);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_13);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_5);
    
						}
						if(("null").equals(replaceStr.toLowerCase())){

    stringBuffer.append(TEXT_14);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(substitution.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_16);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(substitution.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_17);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_18);
    stringBuffer.append(replaceStr);
    stringBuffer.append(TEXT_19);
    
						}else{

    stringBuffer.append(TEXT_20);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(substitution.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_16);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(substitution.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_17);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_18);
    stringBuffer.append(replaceStr);
    stringBuffer.append(TEXT_21);
    
						}
					//for strict match
					}else{
						if(("null").equals(replaceStr.toLowerCase())){
    stringBuffer.append(TEXT_22);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(substitution.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_23);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(substitution.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_17);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_18);
    stringBuffer.append(replaceStr);
    stringBuffer.append(TEXT_18);
    stringBuffer.append(("true").equals(substitution.get("WHOLE_WORD")));
    stringBuffer.append(TEXT_18);
    stringBuffer.append(("true").equals(substitution.get("CASE_SENSITIVE")));
    stringBuffer.append(TEXT_19);
    
						}else{

    stringBuffer.append(TEXT_24);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(substitution.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_23);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(substitution.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_17);
    stringBuffer.append(cid );
    stringBuffer.append(TEXT_3);
    stringBuffer.append(i );
    stringBuffer.append(TEXT_18);
    stringBuffer.append(replaceStr);
    stringBuffer.append(TEXT_25);
    stringBuffer.append(("true").equals(substitution.get("WHOLE_WORD")));
    stringBuffer.append(TEXT_18);
    stringBuffer.append(("true").equals(substitution.get("CASE_SENSITIVE")));
    stringBuffer.append(TEXT_19);
    
						}
					}
                }
            }
        }
    }
    
    
    
    //advanced mode Replacement
    if(("true").equals(advancedMode)) {
        patterns = (List<Map<String,String>>)ElementParameterParser.getObjectValue(node,"__ADVANCED_SUBST__");
        if(patterns != null && patterns.size() > 0) {
            for(Map<String,String> pattern:patterns){
                String replacePat = pattern.get("REPLACE_COLUMN");
                if(replacePat != null && !("").equals(replacePat)) {
                	if(("null").equals(replacePat.toLowerCase())){

    stringBuffer.append(TEXT_26);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(pattern.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_16);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(pattern.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_18);
    stringBuffer.append(pattern.get("SEARCH_COLUMN"));
    stringBuffer.append(TEXT_18);
    stringBuffer.append(pattern.get("REPLACE_COLUMN"));
    stringBuffer.append(TEXT_27);
    }else{
    stringBuffer.append(TEXT_28);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(pattern.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_16);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(pattern.get("INPUT_COLUMN"));
    stringBuffer.append(TEXT_18);
    stringBuffer.append(pattern.get("SEARCH_COLUMN"));
    stringBuffer.append(TEXT_18);
    stringBuffer.append(pattern.get("REPLACE_COLUMN"));
    stringBuffer.append(TEXT_21);
    }
    stringBuffer.append(TEXT_29);
    
                }
            }
        }
    }  
    
    
    if(outgoingConns != null && outgoingConns.size() > 0) {
    	IConnection conn = outgoingConns.get(0);
    	if(conn.getLineStyle().hasConnectionCategory(IConnectionCategory.DATA)) {
	        for(IMetadataColumn metadataColumn : columnList) {
	        
    stringBuffer.append(TEXT_30);
    stringBuffer.append(conn.getName());
    stringBuffer.append(TEXT_15);
    stringBuffer.append(metadataColumn.getLabel());
    stringBuffer.append(TEXT_4);
    stringBuffer.append(incomingConnName);
    stringBuffer.append(TEXT_15);
    stringBuffer.append(metadataColumn.getLabel());
    stringBuffer.append(TEXT_31);
    }
	    }
    }
    
    
    
    stringBuffer.append(TEXT_32);
    stringBuffer.append(cid);
    stringBuffer.append(TEXT_33);
    
}

    stringBuffer.append(TEXT_34);
    return stringBuffer.toString();
  }
}
