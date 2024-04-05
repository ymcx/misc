async function requestPermissions() {
  await chrome.permissions.request({
    origins: ["*://*.youtube.com/*"]
  });
}
document
  .querySelector("#request")
  .addEventListener("click", requestPermissions);
