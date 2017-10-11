
var http = require('http');

var MongoClient = require('mongodb').MongoClient;

var url = "mongodb://localhost:27017/UDB";


function web(req, res)
{
	MongoClient.connect(url, function(err1, db)
	{
		if (err1) throw err1;

		res.writeHead(200, {'Content-Type': 'text/html'});
		res.write("<body>");

		//console.log("Database connection ok");
		var collection = db.collection('users');
		collection.find({}).toArray(function(err2, result)
		{
			if (err2) throw err2;
			for (var post in result)
			{
				//console.log(result[post]);
				res.write("<hr>");
				res.write("name: " + result[post].name + " <br>");
				res.write("pid: "  + result[post].pid + " <br>");
			}
			res.write("<hr>");
			res.end();
			db.close();
		});
	});
}

http.createServer(web).listen(8080); 



