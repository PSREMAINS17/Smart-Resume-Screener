// ================================
// Smart Resume Screening Tool
// script.js
// ================================

document.addEventListener("DOMContentLoaded", () => {

    // ----------------------------
    // Main Score Progress Bar
    // ----------------------------

    const progressBar = document.getElementById("progress-bar");

    if(progressBar){

        const score = progressBar.dataset.score;

        setTimeout(() => {
            progressBar.style.width = score + "%";
        },300);

    }

    // ----------------------------
    // ATS Category Bars
    // ----------------------------

    document.querySelectorAll(".ats-progress").forEach(bar=>{

        const width = bar.dataset.width;

        setTimeout(()=>{

            bar.style.width = width + "%";

        },300);

    });

    // ----------------------------
    // Dark Mode
    // ----------------------------

    const toggle = document.getElementById("darkToggle");

    if(toggle){

        if(localStorage.getItem("theme")==="dark"){

            document.body.classList.add("dark-mode");

            toggle.innerHTML="☀️";

        }

        toggle.addEventListener("click",()=>{

            document.body.classList.toggle("dark-mode");

            if(document.body.classList.contains("dark-mode")){

                localStorage.setItem("theme","dark");

                toggle.innerHTML="☀️";

            }

            else{

                localStorage.setItem("theme","light");

                toggle.innerHTML="🌙";

            }

        });

    }

    // ----------------------------
    // Loading Spinner
    // ----------------------------

    const form=document.querySelector("form");

    if(form){

        form.addEventListener("submit",()=>{

            const loader=document.getElementById("loader");

            if(loader){

                loader.style.display="block";

            }

        });

    }

});