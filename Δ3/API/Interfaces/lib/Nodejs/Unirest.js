var unirest = require("unirest");

var req = unirest("GET", "https://voicerss-text-to-speech.p.rapidapi.com/");

req.query({
	"key": "undefined",
	"src": "Hello, world!",
	"hl": "en-us",
	"r": "0",
	"c": "mp3",
	"f": "8khz_8bit_mono"
});

req.headers({
	"x-rapidapi-key": "SIGN-UP-FOR-KEY",
	"x-rapidapi-host": "voicerss-text-to-speech.p.rapidapi.com",
	"useQueryString": true
});


req.end(function (res) {
	if (res.error) throw new Error(res.error);

	console.log(res.body);
});
