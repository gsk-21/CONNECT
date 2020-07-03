// update_profile_pic

function update_profile_pic() {
	document.querySelector("#profile-pic-form").style.display='block'
	document.querySelector(".profile-pic-btn-remove").style.display = 'none'
	document.querySelector(".profile-pic-btn-update").style.display = 'none'
}


function cancel_update_profile_pic() {
	document.querySelector("#profile-pic-form").style.display = 'none'
	document.querySelector(".profile-pic-btn-remove").style.display = 'inline'
	document.querySelector(".profile-pic-btn-update").style.display = 'inline'
}



