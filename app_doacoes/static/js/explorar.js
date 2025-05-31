document.addEventListener("DOMContentLoaded", () => {
  const description = document.getElementsByClassName("card-text");
  for (let i = 0; i < description.length; i++) {
    if (description[i].innerHTML.length <= 110) continue;
    description[i].innerHTML =
      description[i].innerHTML.substring(0, 110) + "...";
  }
});
