
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


public class QBActivity2MySQL {
    //   private final static ADFLogger logger = ADFLogger.createADFLogger(QBActivity2MySQL.class);

    public QBActivity2MySQL() {
        super();
    }

    public static void main(String[] args) {
        QBActivity2MySQL qBActivity2MySQL = new QBActivity2MySQL();

        final String QBFile = "C:\\Users\\smeng1\\Downloads\\qb.csv";
        final String MySQLString = "jdbc:mysql://www.svcvllc.com:3306/security", MySQLUser = "svcvllc", MySQLPassword =
            "intelinside";
        final String ProjectStr = "Project ";
        
        java.util.Date today = new java.util.Date();
        java.sql.Date timestamp = new java.sql.Date(today.getTime());
        
        FileInputStream fstream = null;
        BufferedReader br = null;
        HashMap svcvUserMap = new HashMap();

        String strLine;

        try {
            fstream = new FileInputStream(QBFile);
            br = new BufferedReader(new InputStreamReader(fstream));
            //Read File Line By Line
        } catch (Exception e) {
            System.err.println(e.getMessage()); // handle exception
        }
        System.out.println("-------- MySQL JDBC Connection Demo ------------");

        try {
            Class.forName("com.mysql.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            System.out.println("MySQL JDBC Driver not found !!");
            return;
        }
        System.out.println("MySQL JDBC Driver Registered!");
        Connection connection = null;
        try {
            connection = DriverManager.getConnection(MySQLString, MySQLUser, MySQLPassword);
            System.out.println("SQL Connection to database established!");

            // Get users first from a readonly query
            Statement statement = connection.createStatement();
            ResultSet rs = statement.executeQuery("SELECT  username, id,email FROM auth_user");
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
                    System.out.print("id=["+rs.getObject(2) +"]\tuserName-[" +  rs.getObject(1)+ "]\t\temail=["+rs.getObject(3));
//                }
                System.out.println("");
            }
            rs.close();
            statement.close();


            // Insert user transactions into the activity table
            PreparedStatement pstmt = null;
            pstmt =
                    connection.prepareStatement("INSERT INTO myapp_investmentactivity " + "(ActivityId, Type_id, date, Memo, Amount, ProjectId_id, Userid_id, createdOn) " +
                                                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
            int lineCounter = 0;
            while ((strLine = br.readLine()) != null) {
                // Print the content on the console
                System.out.println(strLine);

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
                pstmt.setFloat(5, Float.parseFloat(amount[1])); //
                pstmt.setInt(6, Integer.parseInt(projectId)); //
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
            System.out.println("Connection Failed! Check output console");
            e.printStackTrace();
        } catch (IOException e) {
            System.out.println("Read Failed!");
            e.printStackTrace();
        } finally {
            try {
                if (connection != null)
                    connection.close();
                System.out.println("Connection closed !!");

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
}
