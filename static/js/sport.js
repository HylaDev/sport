
function getCookie(name) {
	let cookieValue = null;

	if(document.cookie && document.cookie !== ''){

		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim()

			if (cookie.substring(0, name.length +1 ) === (name + '=')) {

				cookieValue = decodeURIComponent(cookie.substring(0, name.length +1 ));
				break;
			}
		}
	}
	return cookieValue;
}

function retirerNotification(retirerNotificationURL, redirectURL) {
	const csrftoken = getCookie('csrftoken');
	let xmlhttp = new XMLHttpRequest();

	xmlhttp.onreadystatechange = function (){
		if (xmlhttp.readyState ==  XMLHttpRequest.DONE){
			if (xmlhttp.status == 200){
				window.location.replace(redirectURL);
			}else{
				alert('Il y a une erreur');
			}
		}
	};

	xmlhttp.open("DELETE", retirerNotificationURL, true);
	xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
	xmlhttp.send();
}

