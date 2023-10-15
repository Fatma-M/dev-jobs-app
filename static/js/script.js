// UI ELEMENTS
const jobsContainer = document.getElementById("jobs-container");
const loadMoreBtn = document.getElementById("load-more-btn");
const darkModeInput = document.getElementById("darkModeInput");

// GLOBAL VARIABLES
let data;
let darkMode = localStorage.getItem("darkMode")
  ? JSON.parse(localStorage.getItem("darkMode"))
  : false;

function toggleDarkMode() {
  if (darkModeInput.checked) {
    localStorage.setItem("darkMode", true);
    document.body.classList.add("dark");
  } else if (darkModeInput.checked == false) {
    localStorage.setItem("darkMode", false);
    document.body.classList.remove("dark");
  }
}
// Set the checked attribute based on the darkMode state
darkModeInput.checked = darkMode;

toggleDarkMode();
darkModeInput.addEventListener("change", toggleDarkMode);

// CREATE DIV ELEMENTS FOR JOB CARD
function createDiv(element) {
  const div = document.createElement("div");
  div.className =
    "card bg-white dark:bg-darkCardColor p-6 relative flex flex-col items-start justify-between rounded-md mt-[50px]";
  div.innerHTML = `
                  <!-- card image -->
                  <div
                    class="card-image w-[50px] h-[50px] flex items-center rounded-2xl absolute top-[-25px]" style="background: ${element.logoBackground}" >
                    <img src="${element.logo}" alt="" class="block mx-auto"/>
                  </div>
                  <!-- card details -->
                  <div class="time mt-6">
                    <span class="text-darkGray">${element.postedAt}</span>
                    <span class="text-darkGray">.</span>
                    <span class="text-darkGray">${element.contract}</span>
                  </div>
                  <div class="title font-bold my-1">
                    <a class="text-lg" href="/job-details/${element.id}">${element.position}</a>
                  </div>
                  <div class="companyName">
                    <span class="text-darkGray">${element.company}</span>
                  </div>
                  <div class="companyLocation mt-8">
                    <span class="text-darkBlue font-bold">${element.location}</span>
                  </div>
        `;
  jobsContainer.appendChild(div);
}

// UPDATE HOME PAGE WITH DATA FROM THE DATA ROUTE
function updateUI() {
  fetch("/get_data")
    .then((response) => response.json())
    .then((items) => {
      data = items;
      const temp = data.slice(0, 9);
      temp.forEach((element) => {
        createDiv(element);
      });
    })

    .catch((error) => {
      console.error("Error:", error);
    });
}

// HANDLE LOAD MORE DATA
function loadMore() {
  const temp = data.slice(9);

  temp.forEach((element) => {
    createDiv(element);
  });

  loadMoreBtn.style.display = "none";
}

// FUNCTION CALLS AND EVENT LISTENERS
updateUI();
loadMoreBtn.addEventListener("click", loadMore);
