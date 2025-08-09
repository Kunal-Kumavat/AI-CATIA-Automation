function showLoadingMessage(message) {
  const overlay = document.createElement('div');
  overlay.id = 'loading-overlay';
    overlay.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    overlay.innerHTML = `
        <div class="bg-white rounded-lg p-6 flex items-center space-x-3">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-teal-700"></div>
            <span class="text-gray-700">${message}</span>
        </div>
    `;
    document.body.appendChild(overlay);
}



// handle file upload
function submitFileForm() {
  const fileInput = document.getElementById('catpart_file');
  const form = document.getElementById('file_upload_form');

  if (fileInput.files.length > 0) { 
    const file = fileInput.files[0];
    if (file.name.endsWith('.CATPart')) {
      showLoadingMessage('Uploading and opening .CATPart file in CATIA...');
      form.submit();
    } else {
      alert('Please select a .CATPart file');
      fileInput.value = '';
    }
  }
}



function submitTextForm() {
  const textInput = document.getElementById('user_query');  // textarea or input id
  const form = document.getElementById('input_query_form');        // form id

  const text = textInput.value.trim();

  if (text.length > 0) {
    showLoadingMessage('Submitting your query, please wait...');
    form.submit();
  } else {
    alert('Please enter your requirement before submitting.');
    textInput.value = '';
    textInput.focus();
  }
}






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


