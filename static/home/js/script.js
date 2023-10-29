//API url: https://sguaqrtddeaqpoiqarhg.supabase.co
// const mockUserData = {
//     generatedVideos: [
//       { id: 1, title: "Video 1", thumbnail: "video1.jpg" },
//       { id: 2, title: "Video 2", thumbnail: "video2.jpg" },
//       // Add more video objects as needed
//     ]
//   };
  
  
//   // Populate video previews
//   const videoContainer = document.getElementById("videoContainer");
//   const searchInput = document.getElementById("searchInput");
  
//   function renderVideos(videos) {
//     videoContainer.innerHTML = "";
//     videos.forEach(video => {
//       const videoPreview = document.createElement("div");
//       videoPreview.className = "video-preview";
//       videoPreview.innerHTML = `
//         <img src="${video.thumbnail}" alt="${video.title}">
//         <h3>${video.title}</h3>
//       `;
//       videoContainer.appendChild(videoPreview);
//     });
//   }
  
//   renderVideos(mockUserData.generatedVideos);
  
  // Search functionality
  searchInput.addEventListener("input", function () {
    const searchTerm = searchInput.value.toLowerCase();
    const filteredVideos = mockUserData.generatedVideos.filter(video =>
      video.title.toLowerCase().includes(searchTerm)
    );
    renderVideos(filteredVideos);
  });



// Select the profile picture and file input elements
const profilePicture = document.getElementById('profilePicture');
const fileInput = document.getElementById('fileInput');

// Set a change event listener to the file input
fileInput.addEventListener('change', (event) => {
  const selectedFile = event.target.files[0];

  // Check if a file was selected
  if (selectedFile) {
    // Read the selected file as a data URL
    const reader = new FileReader();
    reader.onload = function (e) {
      // Update the profile picture's src with the data URL
      profilePicture.src = e.target.result;
    };
    reader.readAsDataURL(selectedFile);
  }
});




// Select the account info and dropdown menu elements
const accountInfo = document.querySelector('.account-info');
const dropdownMenu = document.querySelector('.dropdown-menu');

// Set a flag to track the menu's visibility
let isDropdownVisible = false;

// Add a click event listener to the account info section
accountInfo.addEventListener('click', (event) => {
  event.stopPropagation(); // Prevent the click from closing the menu
  
  // Toggle the visibility of the dropdown menu
  isDropdownVisible = !isDropdownVisible;
  if (isDropdownVisible) {
    dropdownMenu.style.display = 'block';
  } else {
    dropdownMenu.style.display = 'none';
  }
});

// Close the dropdown menu when the user clicks outside of it
document.addEventListener('click', () => {
  if (isDropdownVisible) {
    dropdownMenu.style.display = 'none';
    isDropdownVisible = false;
  }
});

// Prevent the dropdown menu from closing when clicking inside it
dropdownMenu.addEventListener('click', (event) => {
  event.stopPropagation();
});