
package com.svcvllc.activity;

//import oracle.adf.share.logging.ADFLogger;
import java.io.BufferedReader;
import java.io.FileInputStream;

import java.io.IOException;
import java.io.InputStreamReader;

import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import java.util.ArrayList;
import java.util.HashMap;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;


public class QBActivity2MySQL {
    private static final Log logger=LogFactory.getLog(QBActivity2MySQL.class);
    final static String QBFile = "C:\\Users\\smmeng\\Downloads\\QB-reports\\qb.csv";
    //final static String QBInterestFile = "C:\\Users\\smmeng\\Downloads\\qb-int.csv";
    final static String QBInterestFile = "C:\\Users\\smmeng\\Downloads\\QB-reports\\qb-div.csv";
    final static String MySQLString = "jdbc:mysql://www.svcvllc.com:3306/security", MySQLUser = "smmeng", MySQLPassword ="shanghai0";
    //final static String MySQLString = "jdbc:mysql://sncsmeng03:3306/security", MySQLUser = "smmeng", MySQLPassword ="shanghai0";
    
    final static String ProjectStr = "Project ";
    
    public QBActivity2MySQL() {
        super();
    }
    
    /************************************************************************************************************************************
     * Upload investment principal activities from QB.csv
     ************************************************************************************************************************************/
    static public void uploadPrincipalActivity() {
        java.util.Date today = new java.util.Date();
        java.sql.Date timestamp = new java.sql.Date(today.getTime());
        
        FileInputStream fstream = null;
        BufferedReader br = null;
        HashMap svcvUserMap ;

        String strLine;

        try {
            fstream = new FileInputStream(QBFile);
            br = new BufferedReader(new InputStreamReader(fstream));
            //Read File Line By Line
        } catch (Exception e) {
            logger.error(e.getMessage()); // handle exception
        }
        logger.info("-------- MySQL JDBC Connection Demo ------------");

        try {
            Class.forName("com.mysql.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            logger.info("MySQL JDBC Driver not found !!");
            return;
        }
        logger.info("MySQL JDBC Driver Registered!");
        Connection connection = null;
        try {
            connection = DriverManager.getConnection(MySQLString, MySQLUser, MySQLPassword);
            logger.info("SQL Connection to database established!");
            svcvUserMap = findAllUser(connection);

            // Insert user transactions into the activity table
            PreparedStatement pstmt = null;
            pstmt =
                    connection.prepareStatement("INSERT INTO myapp_investmentactivity " + "(ActivityId, Type_id, date, Memo, Amount, ProjectId_id, Userid_id, createdOn) " +
                                                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
            int lineCounter = 0;
            while ((strLine = br.readLine()) != null) {
                // Print the content on the console
                logger.info(strLine);

                if (null == strLine || strLine.isEmpty())
                    continue;
                String[] fields = strLine.split(",\"");

                if (lineCounter == 0 || fields.length < 3 || null == fields[2] || fields[2].isEmpty() || strLine.toUpperCase().indexOf("CANCEL") > 0) {
                    lineCounter++;
                    continue;
                }

                lineCounter++;

                String[] activityDate = fields[2].split("/");
                String projectId = fields[4];
                projectId = projectId.substring(projectId.indexOf(ProjectStr), projectId.length());
                projectId = projectId.substring(ProjectStr.length(), projectId.indexOf("-"));

                String userName = fields[3].substring(fields[3].indexOf("(") + 1, fields[3].indexOf(")"));
                ArrayList user = (ArrayList)svcvUserMap.get(userName.toUpperCase());
                Integer userId = (Integer)user.get(0);
                
                String memo = fields[4].replaceAll("\"", ""); 
                memo = memo.replaceFirst(ProjectStr + projectId+"-", "");

                String[] amount = fields[5].split(",");
                pstmt.setInt(1, 0);
                pstmt.setString(2, fields[1].replaceAll("\"", ""));
                pstmt.setString(3, activityDate[2] + "-" + activityDate[0] + "-" + activityDate[1]); //
                pstmt.setString(4, memo); //
                pstmt.setFloat(5, Float.parseFloat(amount[1].trim())); //
                pstmt.setInt(6, Integer.parseInt(projectId.trim())); //
                pstmt.setInt(7, userId.intValue()); //
                pstmt.setDate(8, timestamp); //
                pstmt.addBatch();
                //pstmt.executeUpdate();
            }
            pstmt.executeBatch();

            if (pstmt != null)
                pstmt.close();

            //connection.commit();  // auto-commit is on
        } catch (SQLException e) {
            logger.info("Connection Failed! Check output console");
            e.printStackTrace();
        } catch (IOException e) {
            logger.info("Read Failed!");
            e.printStackTrace();
        } finally {
            try {
                if (connection != null)
                    connection.close();
                logger.info("Connection closed !!");

                if (br != null) {
                    try {
                        //Close the input stream
                        br.close();
                        logger.info("Successfully import all activities!!");
                    } catch (Throwable t) { /* ensure close happens */
                    }
                }

            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
        
    }

    /************************************************************************************************************************************
     * Upload interest activities from QB-int.csv
     ************************************************************************************************************************************/
    static public void uploadInterestActivity() {
        
        java.util.Date today = new java.util.Date();
        java.sql.Date timestamp = new java.sql.Date(today.getTime());
        
        FileInputStream fstream = null;
        BufferedReader br = null;
        HashMap svcvUserMap;

        String strLine;

        try {
            fstream = new FileInputStream(QBInterestFile);
            br = new BufferedReader(new InputStreamReader(fstream));
            //Read File Line By Line
        } catch (Exception e) {
            logger.error(e.getMessage()); // handle exception
        }
        logger.info("-------- MySQL JDBC Connection for Interest ------------");

        try {
            Class.forName("com.mysql.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            logger.info("MySQL JDBC Driver not found !!");
            return;
        }
        logger.info("MySQL JDBC Driver Registered!");
        Connection connection = null;
        try {
            connection = DriverManager.getConnection(MySQLString, MySQLUser, MySQLPassword);
            logger.info("SQL Connection to database established!");

            svcvUserMap = findAllUser(connection);

            // Insert user transactions into the activity table
            PreparedStatement pstmt = null;
            pstmt =
                    connection.prepareStatement("INSERT INTO myapp_investmentactivity " + "(ActivityId, Type_id, date, Memo, Amount, ProjectId_id, Userid_id, createdOn) " +
                                                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
            int lineCounter = 0;
            while ((strLine = br.readLine()) != null) {
                // Print the content on the console
                logger.info(strLine);

                if (null == strLine || strLine.isEmpty())
                    continue;
                String[] fields = strLine.split(",\"");// not ," as separator

                if (lineCounter == 0 || fields.length < 3 || null == fields[2] || fields[2].isEmpty() || strLine.toUpperCase().indexOf("CANCEL") > 0) {
                    lineCounter++;
                    continue;
                }

                lineCounter++;

                String[] activityDate = fields[2].split("/");

                String projectId ;
                projectId = fields[4];
                    
                projectId = projectId.substring(projectId.indexOf(ProjectStr), projectId.length());
                projectId = projectId.substring(ProjectStr.length(), projectId.indexOf("-"));

                String userName = fields[3].substring(fields[3].indexOf("(") + 1, fields[3].indexOf(")"));
                ArrayList user = (ArrayList)svcvUserMap.get(userName.toUpperCase());
                Integer userId = (Integer)user.get(0);
                
                String memo = fields[4].replaceAll("\"", ""); 
                memo = memo.replaceFirst(ProjectStr + projectId+"-", "");

                String[] amount = fields[5].split(",");
                pstmt.setInt(1, 0);
                if (QBInterestFile!=null && QBInterestFile.toLowerCase().indexOf("int")>-1)
                    pstmt.setString(2, "Interest");//fields[1].replaceAll("\"", ""));
                else
                    pstmt.setString(2, "Dividend");//fields[1].replaceAll("\"", ""));
                
                pstmt.setString(3, activityDate[2] + "-" + activityDate[0] + "-" + activityDate[1]); //
                pstmt.setString(4, memo); //
                pstmt.setFloat(5, Float.parseFloat(amount[1].trim())); //
                pstmt.setInt(6, Integer.parseInt(projectId.trim())); //
                pstmt.setInt(7, userId.intValue()); //
                pstmt.setDate(8, timestamp); //
                pstmt.addBatch();
                //pstmt.executeUpdate();
            }
            pstmt.executeBatch();

            if (pstmt != null)
                pstmt.close();

            //connection.commit();  // auto-commit is on
        } catch (SQLException e) {
            logger.info("Connection Failed! Check output console");
            e.printStackTrace();
        } catch (IOException e) {
            logger.info("Read Failed!");
            e.printStackTrace();
        } finally {
            try {
                if (connection != null)
                    connection.close();
                logger.info("Connection closed !!");

                if (br != null) {
                    try {
                        //Close the input stream
                        br.close();
                    } catch (Throwable t) { /* ensure close happens */
                    }
                }

            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
        
    }
    
    /************************************************************************************************************************************
     * prepare a list of investors from MySQL before uploading any activites
     ************************************************************************************************************************************/
    static private HashMap findAllUser(Connection connection) {
        HashMap svcvUserMap = null;
        Statement statement = null;
        ResultSet rs = null;

        try
        {
            // Get users first from a readonly query
            statement = connection.createStatement();
            rs = statement.executeQuery("SELECT  username, id,email FROM auth_user");
            svcvUserMap = new HashMap();
            while (rs.next()) {
    
                ArrayList user = new ArrayList();
                user.add(rs.getObject(2));
                user.add(rs.getObject(3));
                svcvUserMap.put(rs.getObject(1).toString().toUpperCase(), user);
            //                for (int i = 1; i <= numColumns; i++) {
                    // Column numbers start at 1.
                    // Also there are many methods on the result set to return
                    //  the column as a particular type. Refer to the Sun documentation
                    //  for the list of valid conversions.
                    logger.info("id=["+rs.getObject(2) +"]\tuserName-[" +  rs.getObject(1)+ "]\t\temail=["+rs.getObject(3));
            //                }
                logger.info("");
            }
            rs.close();
            statement.close();
        
        } catch (SQLException e) {
            logger.info("Connection Failed! Check output console");
            e.printStackTrace();
        }
        finally {
            try
            {
                if (rs != null)
                    rs.close();
                
                if (statement != null)
                    statement.close();
            
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
        return svcvUserMap;
    }

    public static void main(String[] args) {
        //QBActivity2MySQL.uploadPrincipalActivity();
        QBActivity2MySQL.uploadInterestActivity();// can be used for dividends too
    }

        
}
