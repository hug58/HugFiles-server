const gear = document.querySelector('.gear');
const options = document.querySelector('.options');

gear.addEventListener('click', () => {
  options.style.display = options.style.display === 'none' ? 'block' : 'none';
});

function bytesToMB(bytes) {
  const mb = bytes / (1024 * 1024);
  return mb.toFixed(2);
}

function unixTimestampToDateString(timestamp) {
  const date = new Date(timestamp * 1000);
  const dateString = date.toISOString().slice(0, 10);
  return dateString;
}