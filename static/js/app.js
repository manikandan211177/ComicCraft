/*
=========================================================
ComicCraft - AI Comic Story Creator
Main JavaScript
=========================================================
*/

"use strict";


/* ======================================================
   DOM READY
   ====================================================== */

document.addEventListener("DOMContentLoaded", function () {

    initializeForm();

    initializeDownloadButtons();

    initializeImageHandling();

    initializeTextareaCounter();

});


/* ======================================================
   FORM HANDLING
   ====================================================== */

function initializeForm() {

    const form = document.querySelector(".comic-form");

    if (!form) {
        return;
    }


    form.addEventListener("submit", function (event) {

        const storyPrompt =
            document.getElementById("story_prompt");

        const characterName =
            document.getElementById("character_name");

        const setting =
            document.getElementById("setting");

        const tone =
            document.getElementById("tone");

        const artStyle =
            document.getElementById("art_style");


        /*
        Basic client-side validation
        */

        if (
            !storyPrompt ||
            !characterName ||
            !setting ||
            !tone ||
            !artStyle
        ) {
            return;
        }


        if (storyPrompt.value.trim().length === 0) {

            event.preventDefault();

            showClientError(
                "Please enter a story prompt."
            );

            storyPrompt.focus();

            return;
        }


        if (characterName.value.trim().length === 0) {

            event.preventDefault();

            showClientError(
                "Please enter a main character name."
            );

            characterName.focus();

            return;
        }


        if (setting.value === "") {

            event.preventDefault();

            showClientError(
                "Please select a setting."
            );

            setting.focus();

            return;
        }


        if (tone.value === "") {

            event.preventDefault();

            showClientError(
                "Please select a story tone."
            );

            tone.focus();

            return;
        }


        if (artStyle.value === "") {

            event.preventDefault();

            showClientError(
                "Please select an art style."
            );

            artStyle.focus();

            return;
        }


        /*
        Prevent multiple submissions.
        */

        const button =
            form.querySelector(
                'button[type="submit"]'
            );


        if (button) {

            button.disabled = true;

            button.innerHTML =
                "⏳ Creating Your Comic...";

        }


        /*
        Show loading screen.
        */

        showLoadingOverlay();

    });

}


/* ======================================================
   CLIENT ERROR
   ====================================================== */

function showClientError(message) {

    let errorBox =
        document.querySelector(".client-error");


    if (!errorBox) {

        errorBox =
            document.createElement("div");

        errorBox.className =
            "error-message client-error";


        const form =
            document.querySelector(".comic-form");


        if (form) {

            form.parentNode.insertBefore(
                errorBox,
                form
            );

        }

    }


    errorBox.innerHTML =
        "<strong>Error:</strong> " +
        escapeHtml(message);


    errorBox.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


/* ======================================================
   LOADING OVERLAY
   ====================================================== */

function showLoadingOverlay() {

    let overlay =
        document.querySelector(".loading-overlay");


    if (!overlay) {

        overlay =
            document.createElement("div");

        overlay.className =
            "loading-overlay";


        overlay.innerHTML = `
            <div class="loading-box">

                <div class="spinner"></div>

                <h3>
                    Creating Your Comic
                </h3>

                <p>
                    Gemini is writing your story
                    and generating your comic panels...
                </p>

            </div>
        `;


        document.body.appendChild(overlay);

    }


    requestAnimationFrame(function () {

        overlay.classList.add("active");

    });

}


/* ======================================================
   DOWNLOAD BUTTONS
   ====================================================== */

function initializeDownloadButtons() {

    const buttons =
        document.querySelectorAll(
            ".download-button"
        );


    buttons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const originalText =
                    button.innerHTML;


                button.innerHTML =
                    "⏳ Preparing PDF...";


                button.style.pointerEvents =
                    "none";


                /*
                Restore button after a short delay.
                The browser handles the actual download.
                */

                setTimeout(function () {

                    button.innerHTML =
                        originalText;

                    button.style.pointerEvents =
                        "";

                }, 2500);

            }
        );

    });

}


/* ======================================================
   IMAGE ERROR HANDLING
   ====================================================== */

function initializeImageHandling() {

    const images =
        document.querySelectorAll(
            ".panel-image"
        );


    images.forEach(function (image) {

        image.addEventListener(
            "error",
            function () {

                const container =
                    image.parentElement;


                if (!container) {
                    return;
                }


                image.style.display =
                    "none";


                const placeholder =
                    document.createElement("div");


                placeholder.className =
                    "image-placeholder";


                placeholder.innerHTML = `
                    <span>🖼️</span>
                    <p>
                        Unable to load this panel image.
                    </p>
                `;


                container.appendChild(
                    placeholder
                );

            }
        );

    });

}


/* ======================================================
   TEXTAREA CHARACTER COUNTER
   ====================================================== */

function initializeTextareaCounter() {

    const textarea =
        document.getElementById(
            "story_prompt"
        );


    if (!textarea) {
        return;
    }


    const maxLength =
        parseInt(
            textarea.getAttribute("maxlength"),
            10
        );


    if (!maxLength) {
        return;
    }


    const counter =
        document.createElement("small");


    counter.className =
        "character-counter";


    counter.style.display =
        "block";


    counter.style.textAlign =
        "right";


    counter.style.color =
        "#888";


    counter.style.marginTop =
        "4px";


    textarea.parentNode.appendChild(
        counter
    );


    function updateCounter() {

        const currentLength =
            textarea.value.length;


        counter.textContent =
            currentLength +
            " / " +
            maxLength;

    }


    textarea.addEventListener(
        "input",
        updateCounter
    );


    updateCounter();

}


/* ======================================================
   ESCAPE HTML
   ====================================================== */

function escapeHtml(value) {

    const div =
        document.createElement("div");


    div.textContent =
        value;


    return div.innerHTML;

}


/* ======================================================
   CONFIRMATION BEFORE LEAVING
   ====================================================== */

let comicGenerationStarted = false;


document.addEventListener(
    "submit",
    function (event) {

        if (
            event.target &&
            event.target.classList &&
            event.target.classList.contains(
                "comic-form"
            )
        ) {

            comicGenerationStarted = true;

        }

    }
);


/* ======================================================
   KEYBOARD SHORTCUT
   ====================================================== */

document.addEventListener(
    "keydown",
    function (event) {

        /*
        Ctrl + Enter submits the comic form.
        */

        if (
            event.ctrlKey &&
            event.key === "Enter"
        ) {

            const form =
                document.querySelector(
                    ".comic-form"
                );


            if (form) {

                form.requestSubmit();

            }

        }

    }
);