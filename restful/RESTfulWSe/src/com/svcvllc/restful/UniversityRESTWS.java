package com.svcvllc.restful;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;

@Path("/university")
public class UniversityRESTWS {

		@GET
		@Produces(MediaType.TEXT_HTML)
		public String getHTMLUniversity() {
			return "<html> <title> Univ. Info </title> <body> <h1> University Info </h1> </body> </html>";
		}

		@GET
		@Path("/getXML")
		@Produces(MediaType.TEXT_PLAIN)
		public String getXMLUniversity() {
			return "Name - University Info";
		}

		@PUT
	    @Consumes("text/plain")
		@Path("/{studentRollNo}/{name}")
		@Produces(MediaType.TEXT_PLAIN)
		public String updateLUniversityInfo(@PathParam("studentRollNo") String studentRollNo, 
				@PathParam("name") String name) {
			return "Updated successfully for studentRollNo["+studentRollNo + "] name=["+name;
		}

}
