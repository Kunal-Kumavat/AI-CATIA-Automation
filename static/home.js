// document.addEventListener('DOMContentLoaded', function () {
//   const fileInput = document.getElementById('fileInput');
//   const uploadBtn = document.getElementById('uploadBtn');
//   const progressContainer = document.getElementById('progressContainer');
//   const progressBar = document.getElementById('progressBar');
//   const progressText = document.getElementById('progressText');

//   let selectedFile = null;

//   fileInput.addEventListener('change', function () {
//     selectedFile = fileInput.files[0] || null;
//     progressBar.style.width = '0%';
//     progressContainer.classList.add('hidden');
//     progressText.textContent = '';
//   });

//   uploadBtn.addEventListener('click', function () {
//     if (!selectedFile) {
//       alert('Please select a file first!');
//       return;
//     }

//     // Show progress bar
//     progressContainer.classList.remove('hidden');
//     progressBar.style.width = '0%';
//     progressText.textContent = 'Uploading...';

//     // Simulate upload to a server (replace with your endpoint)
//     const formData = new FormData();
//     formData.append('file', selectedFile);

//     // Example: Replace with your actual endpoint
//     const uploadUrl = 'https://httpbin.org/post'; // For demo, use httpbin

//     const xhr = new XMLHttpRequest();
//     xhr.open('POST', uploadUrl, true);

//     // Progress event
//     xhr.upload.addEventListener('progress', function (e) {
//       if (e.lengthComputable) {
//         const percent = Math.round((e.loaded / e.total) * 100);
//         progressBar.style.width = percent + '%';
//         progressText.textContent = `Uploading: ${percent}%`;
//       }
//     });

//     xhr.onload = function () {
//       if (xhr.status === 200) {
//         progressBar.style.width = '100%';
//         progressText.textContent = 'Upload complete!';
//       } else {
//         progressText.textContent = 'Upload failed.';
//       }
//     };

//     xhr.onerror = function () {
//       progressText.textContent = 'Upload failed.';
//     };

//     xhr.send(formData);
//   });
// });


function redirectToCatia() {
  window.location.href = '/catia_automation';
}


document.getElementById("new_chat").addEventListener("click", function() {
    window.location.href = "/home";
})



document.getElementById("profile").addEventListener("click", function() {
    window.location.href = "/profile";
})


