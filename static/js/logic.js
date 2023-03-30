 // Get the "My projects" link element by its ID
  const myProjectsLink = document.getElementById("my-projects-link");

  // Add a click event listener to the link
  myProjectsLink.addEventListener("click", function() {
    // Remove the "active" class from the "All projects" link
    const allProjectsLink = document.querySelector(".nav-link.active");
    allProjectsLink.classList.remove("active");

    // Add the "active" class to the "My projects" link
    myProjectsLink.classList.add("active");
  });