//Client side validation for registration form
function validateRegistrationForm()
{
	var username = document.forms["registration_form"]["username"].value;
	var email = document.forms["registration_form"]["email"].value;
	var	password = document.forms["registration_form"]["password"].value;
	var password2 = document.forms["registration_form"]["password2"].value;
	var ret = true
	//Username Validation
	//Check if empty
	if (username == "")
	{
		document.getElementById("username_validate_msg").innerHTML = "ERROR: Empty Username Field"
		ret = false
	}
	else
	{
		document.getElementById("username_validate_msg").innerHTML = null
	}
	//Email Validation
	//Check against regular expression to see if it's a valid email
	var regular_expression = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	if(regular_expression.test(String(email).toLowerCase()) == false)
	{
		document.getElementById("email_validate_msg").innerHTML = "ERROR: Invalid Email"
		ret = false
	}
	else
	{
		document.getElementById("email_validate_msg").innerHTML = null
	}
	//Pasword Validation
	//Check if the 2 password's match
	if (password != password2)
	{
		document.getElementById("password_validate_msg").innerHTML = "ERROR: Passwords do not match"
		ret = false
	}
	//Check if password field is emtpy
	else if (password == "")
	{
		document.getElementById("password_validate_msg").innerHTML = "ERROR : Empty Password Field"
		ret = false
	}
	else
	{
		document.getElementById("password_validate_msg").innerHTML = null
	}
	//Check if second password field is empty
	if (password2 == "")
	{
		document.getElementById("password2_validate_msg").innerHTML = "ERROR: Empty Second Password Field"
		ret = false
	}
	else
	{
		document.getElementById("password2_validate_msg").innerHTML = null
	}
	return ret
}

//Client side validation for login
function validateLoginForm()
{
	var username = document.forms["login_form"]["username"].value;
	var password = document.forms["login_form"]["password"].value;
	var ret = true
	//Username Validation
	//Check if field is emtpy
	if (username == "")
	{
		document.getElementById("username_validate_msg").innerHTML = "ERROR: Empty Username Field"
		ret = false
	}
	else
	{
		document.getElementById("username_validate_msg").innerHTML = null
	}
	//Pasword Validation
	//Check if field is empty
	if (password == "")
	{
		document.getElementById("password_validate_msg").innerHTML = "ERROR : Empty Password Field"
		ret = false
	}
	else
	{
		document.getElementById("password_validate_msg").innerHTML = null
	}
	return ret
}

//Client side validation for creating a quiz 
function validateQuizForm()
{
	var name = document.forms["quiz_form"]["name"].value;
	var image = document.forms["quiz_form"]["image"].value;
	var ret = true
	//Quiz name validation
	//Check if field is empty
	if (name == "")
	{
		document.getElementById("name_validate_msg").innerHTML = "ERROR: Empty Username Field"
		ret = false
	}
	else
	{
		document.getElementById("name_validate_msg").innerHTML = null
	}
	//Image Validation
	//Check if field is empty
	if (image == "")
	{
		document.getElementById("image_validate_msg").innerHTML = "ERROR : Empty Password Field"
		ret = false
	}
	//Check if image link ends with .jpeg,.jpg, or .png
	else if (image.match(/\.(jpeg|jpg|png)$/) == null)
	{
		document.getElementById("image_validate_msg").innerHTML = "ERROR: Image path given doesn't end in .jpeg/jpg/png"
		ret = false
	}
	else
	{
		document.getElementById("image_validate_msg").innerHTML = null
	}
	return ret
}

//Function to check if we have a valid video id and embed access is enabled
function checkVidID()
{
	var youtube_link = document.forms["question_form"]["youtube_link"].value;
	//Youtube link validation
	if (youtube_link.startsWith("https://www.youtube.com/watch?v="))
	{
		//Shorten youtube_link for database purposes + video_id indexing
		document.getElementById("youtube_link").value = youtube_link.replace("https://www.youtube.com/watch?v=","https://youtu.be/")
		document.getElementById("youtube_link_validate_message").innerHTML = "Modified Youtube Link for compatibility. Original Link : " + youtube_link
		video_id = document.getElementById("youtube_link").value.slice(17,);
		//Embed the video into video player to see if it works
		var source = "https://www.youtube.com/embed/".concat(video_id,"?enablejsapi=1")
		document.getElementById("player").src = source
	}
	else if (youtube_link.startsWith("https://youtu.be/"))
	{
		document.getElementById("youtube_link_validate_message").innerHTML = null
		video_id = youtube_link.slice(17,);
		//Embed the video into video player to see if it works
		var source = "https://www.youtube.com/embed/".concat(video_id,"?enablejsapi=1")
		document.getElementById("player").src = source
	}
	else
	{
		document.getElementById("youtube_link_validate_message").innerHTML = "ERROR: Invalid link must be of format https://youtu.be/video_id or https://www.youtube.com/watch?v=video_id"
	}
}

//Create Question Form Validation
function validateQuestionForm()
{
	var youtube_link = document.forms["question_form"]["youtube_link"].value;
	var start_time = document.forms["question_form"]["start_time"].value;
	var duration = document.forms["question_form"]["duration"].value;
	var correct_answer = document.forms["question_form"]["correct_answer"].value;
	var option_1 = document.forms["question_form"]["option_1"].value;
	var option_2 = document.forms["question_form"]["option_2"].value;
	var option_3 = document.forms["question_form"]["option_3"].value;	
	var ret = true
	//Youtube link validation
	//Shorten youtube link if necessary and notify user of modification
	if (youtube_link.startsWith("https://www.youtube.com/watch?v="))
	{
		document.getElementById("youtube_link").value = youtube_link.replace("https://www.youtube.com/watch?v=","https://youtu.be/")
		document.getElementById("youtube_link_validate_message").innerHTML = "Modified Youtube Link for compatibility. Original Link : " + youtube_link
	}
	else if (youtube_link.startsWith("https://youtu.be/"))
	{
		document.getElementById("youtube_link_validate_message").innerHTML = null
	}
	//Not a valid youtube link
	else
	{
		document.getElementById("youtube_link_validate_message").innerHTML = "ERROR: Invalid link must be of format https://youtu.be/video_id or https://www.youtube.com/watch?v=video_id"
	}
	
	//Start_time validation
	//Check that a number is given
	if (Number.isNaN(Number(start_time)))
	{
		document.getElementById("start_time_validate_message").innerHTML = "ERROR: Value for Video start time isn't an integer"
		ret = false
	}
	//Check to ensure integer is positive
	else if (Number(start_time) < 0)
	{
		document.getElementById("start_time_validate_message").innerHTML = "ERROR: Value for Video start time isn't positive"
		ret = false
	}
	//Check to ensure that the number is an integer
	else if (Number.isInteger(Number(start_time)) == false)
	{
		document.getElementById("start_time_validate_message").innerHTML = "ERROR: Value for Video start time isn't an integer"
		ret = false
	}
	else
	{
		document.getElementById("start_time_validate_message").innerHTML = null
	}

	//Duration validation
	//Check that a number is given
	if (Number.isNaN(Number(duration)))
	{
		document.getElementById("duration_validate_message").innerHTML = "ERROR: Value for playtime isn't an integer"
		ret = false
	}
	//Check that it's positive
	else if (Number(duration) < 0)
	{
		document.getElementById("duration_validate_message").innerHTML = "ERROR: Value for playtime isn't positive"
		ret = false
	}
	//Check that it's an integer
	else if (Number.isInteger(Number(duration)) == false)
	{
		document.getElementById("duration_validate_message").innerHTML = "ERROR: Value for playtime isn't an integer"
		ret = false
	}
	else
	{
		document.getElementById("duration_validate_message").innerHTML = null
	}
	return ret
}

//User Question Answer Form Validation
function validateQuizQuestionForm()
{
	ret = true
	var answer = document.forms["quiz_question_form"]["answer"].value;
	//Check to ensure that the user doesn't select no answer before moving onto next question
	if (answer == "None")
	{
		document.getElementById("answer_validate_message").innerHTML = "ERROR: Please select a valid answer"
		ret = false
	}
	else
	{
		document.getElementById("answer_validate_message").innerHTML = null
	}
	return ret
}
