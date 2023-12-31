// UI ELEMENTS
const jobsContainer = document.getElementById("jobs-container");
const loadMoreBtn = document.getElementById("load-more-btn");
const darkModeInput = document.getElementById("darkModeInput");
const filterByTitleInput = document.getElementById("filter-by-title");
const filterByLocationInput = document.getElementById("filter-by-location");
const filterByFulltimeInput = document.getElementById("filter-by-fulltime");

// GLOBAL VARIABLES
let data;
let darkMode = localStorage.getItem("darkMode")
  ? JSON.parse(localStorage.getItem("darkMode"))
  : false;

// HANDLE DARK MODE AND SET USER CHOICE TO LOCAL STORAGE
function handleDarkMode() {
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

// CREATE DIV ELEMENT FOR JOB CARD
function createDiv(element) {
  const div = document.createElement("div");
  div.className =
    "card bg-white dark:bg-darkCardColor p-6 relative flex flex-col items-start justify-between rounded-md mt-[50px] cursor-pointer";

  div.innerHTML = `
                <a href='/job-details/${element.id}' target="_blank">
                  <!-- card image -->
                  <div
                    class="card-image w-[50px] h-[50px] flex items-center rounded-2xl absolute top-[-25px]" style="background: ${element.logoBackground}" >
                    <img src="${element.logo}" alt="" class="block mx-auto" />
                  </div>
                  <!-- card details -->
                  <div class="time mt-6">
                    <span class="text-darkGray">${element.postedAt}</span>
                    <span class="text-darkGray">.</span>
                    <span class="text-darkGray">${element.contract}</span>
                  </div>
                  <div class="title font-bold my-1">
                    <p class="text-lg">${element.position}</p>
                  </div>
                  <div class="companyName">
                    <span class="text-darkGray">${element.company}</span>
                  </div>
                  <div class="companyLocation mt-8">
                    <span class="text-darkBlue font-bold">${element.location}</span>
                  </div>
                </a>
        `;

  jobsContainer.appendChild(div);
}

// UPDATE HOME PAGE WITH DATA FROM THE DATA ROUTE
function updateUI() {
  fetch("/get_data")
    .then((response) => response.json())
    .then((items) => {
      data = items;
      data.reverse();
      const temp = data.slice(0, 9);
      temp.forEach((element) => {
        createDiv(element);
      });
    })

    .catch((error) => {
      console.error("Error:", error);
    });
}

// FILTER BY TITLE, LOCATION AND FULLTIME HANDLE
function searchJobs() {
  const location = filterByLocationInput.value.toLowerCase();
  const title = filterByTitleInput.value.toLowerCase();
  const fulltime = filterByFulltimeInput.checked;

  const filteredByTitleAndPosition = data.filter((job) => {
    return (
      job.position.toLowerCase().includes(title) &&
      job.location.toLowerCase().includes(location)
    );
  });

  const selectedJobs = filteredByTitleAndPosition.filter((job) => {
    if (fulltime) {
      return job.contract.includes("Full");
    } else {
      return job.contract;
    }
  });

  jobsContainer.innerHTML = " ";
  loadMoreBtn.style.display = "none";
  selectedJobs.forEach((job) => {
    createDiv(job);
  });

  if (selectedJobs.length < 1) {
    jobsContainer.innerHTML = `
    <h1 class="text-red-700 w-full text-center text-2xl col-span-4 mt-4">
    No data found for this search.
  </h1> 
    `;
  }
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
if (jobsContainer != null) {
  updateUI();
  loadMoreBtn.addEventListener("click", loadMore);
  [filterByTitleInput, filterByLocationInput, filterByFulltimeInput].forEach(
    (input) => {
      input.addEventListener("input", searchJobs);
    }
  );
}

handleDarkMode();
darkModeInput.addEventListener("change", handleDarkMode);
