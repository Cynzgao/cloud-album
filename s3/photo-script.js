
var apigClient = apigClientFactory.newClient();
window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;

// Checking if SpeechRecognition is supported by the browser
if ('SpeechRecognition' in window) {
  console.log("SpeechRecognition is Working");
} else {
  console.log("SpeechRecognition is Not Working");
}

// Setting Speech Recognition Properties
const recognition = new window.SpeechRecognition();
recognition.lang = 'en-US';

var albumBucketName = "photos-hw3b2";
var bucketRegion = "us-east-1";
var IdentityPoolId = "us-east-1:1d1dcf51-2480-469d-bf87-510a2fad15e7";

AWS.config.update({
  region: bucketRegion,
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: IdentityPoolId
  })
});

var s3 = new AWS.S3({
  apiVersion: "2006-03-01",
  params: { Bucket: albumBucketName }
});

recognition.onresult = (event) => {
  const speechToText = event.results[0][0].transcript;
  console.log(speechToText);
  searchResults(speechToText);
}

function voiceSearchPhoto() {
  recognition.start();
  console.log("Ready to receive a voice command");
}

function textSearchPhoto() {
  var searchText = document.getElementById('search-input').value.trim().toLowerCase();
  if(searchText == "") {
    alert("Please enter valid text");
  } else {
    searchResults(searchText);
  }
}

function searchResults(searchText) {
  document.getElementById('output-box').innerHTML = "";
  document.getElementById('search-input').value = searchText;
  var searchResults = [];
  var params = {
    'q': searchText
  };
  var body = {};
  var additionalParams = {
    headers: {
      'x-api-key': 'YOUR API KEY'
    },
    queryParams: {}
  };
  return apigClient.searchGet(params,body,additionalParams)
  .then(function(result){
    console.log(result);
    var items = result.data;
    console.log(typeof result.data);
    Array.prototype.forEach.call(items, element=>{
      searchResults.push(element);
    });
    searchResults.forEach(function(element)  {
      document.getElementById('output-box').innerHTML += "<img src=\"https://s3.amazonaws.com/photos-hw3b2/"+element+"\" width=\"50%\" height=\"50%\" style=\"border-radius: 10px\">";
    });
    if(searchResults.length == 0){
      document.getElementById('output-box').innerHTML = "<p align=\"center\"><STRONG>NO SEARCH RESULTS FOUND</STRONG></p>";
    }
  })
  .catch(function(error){
    console.log(error);
  });
}

function s3upload() {
   var files = document.getElementById('fileUpload').files;
   if (files) 
   {
     var file = files[0];
     var fileName = file.name;
     s3.upload({
        Key: fileName,
        Body: file,
        ACL: 'public-read'
        }, function(err, data) {
        if(err) {
        reject('error');
        }
        alert('Successfully Uploaded!');
        }).on('httpUploadProgress', function (progress) {
        var uploaded = parseInt((progress.loaded * 100) / progress.total);
        $("progress").attr('value', uploaded);
      });
   }
};




