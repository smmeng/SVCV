package com.svcvllc.activity;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class HttpURLCOnnectionExample {
    private static final Log logger=LogFactory.getLog(HttpURLCOnnectionExample.class);
    private static final String USER_AGENT = "Mozilla/5.0";
    
    private static final String GET_URL = "http://bbs.wenxuecity.com/tzlc/1112015.html";
    
    private static final String POST_URL = "http://localhost:9090/SpringMVCExample/home";
    
    private static final String POST_PARAMS = "userName=raj";
    
    public static void main(String[] args) throws IOException {
    
        try
        {
            for (int i =0; i < 130;i++)
            {
                sendGET();
                Thread.sleep(5000);
            }
        }
        catch (InterruptedException ex) { ex.printStackTrace(); }
        logger.info("GET DONE");
        //sendPOST();
        //logger.info("POST DONE");
    }
    
    private static void sendGET() throws IOException {
        URL obj = new URL(GET_URL);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();
        con.setRequestMethod("GET");
        con.setRequestProperty("User-Agent", USER_AGENT);
        int responseCode = con.getResponseCode();
        logger.info("GET Response Code :: " + responseCode);
        if (responseCode == HttpURLConnection.HTTP_OK) { // success
            BufferedReader in = new BufferedReader(new InputStreamReader(
                    con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();
    
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
    
            // print result
            logger.info(response.toString());
        } else {
            logger.info("GET request not worked");
        }
    
    }
    
    private static void sendPOST() throws IOException {
        URL obj = new URL(POST_URL);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("User-Agent", USER_AGENT);
    
        // For POST only - START
        con.setDoOutput(true);
        OutputStream os = con.getOutputStream();
        os.write(POST_PARAMS.getBytes());
        os.flush();
        os.close();
        // For POST only - END
    
        int responseCode = con.getResponseCode();
        logger.info("POST Response Code :: " + responseCode);
    
        if (responseCode == HttpURLConnection.HTTP_OK) { //success
            BufferedReader in = new BufferedReader(new InputStreamReader(
                    con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();
    
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
    
            // print result
            logger.info(response.toString());
        } else {
            logger.info("POST request not worked");
        }
    }
}
