function updatePreview() {
  // existing code...

  // Profile image preview
  const file = profileImageField.files[0];
  const previewImg = document.getElementById("profilePreview");
  if (file && (file.type === "image/jpeg" || file.type === "image/png")) {
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImg.src = e.target.result;
      previewImg.style.display = "block";
    };
    reader.readAsDataURL(file);
  } else {
    previewImg.src = "";
    previewImg.style.display = "none";
  }
}
