const playBtn = document.querySelector(".play"),
    skipForward = document.querySelector(".skip-forward"),
    skipBack = document.querySelector(".skip-back"),

    progressBarContainer = document.querySelector('.progress'),
    progressBar = document.querySelector('.progress-bar'),
    progressHead = document.querySelector('.progress-head'),

    currentTimeHtml = document.querySelector(".current-time"),
    durationHtml = document.querySelector(".duration"),

    playIcon = document.querySelector('.fa-play'),
    img = document.querySelector('.img'),
    video = document.querySelector('.video'),
    title = document.querySelector(".audio-title"),
    singer = document.querySelector(".audio-singer");

this.tracks = [
    {
        name: "Tech House vibes",
        artist: "Artist 1",
        cover: "",
        source: "/static/results/merge.mp4",
    },
    {
        name: "Tech House vibes",
        artist: "Artist 1",
        cover: "/static/results/man1.jpg",
        source: "/static/results/man1.mp4",
    },
    {
        name: "Hip Hop 02",
        artist: "Artist 2",
        cover: "/static/results/man2.jpg",
        source: "/static/results/man2.mp4",
    },
    {
        name: "Dreaming Big",
        artist: "Artist 3",
        cover: "/static/results/man3.jpg",
        source: "/static/results/man3.mp4",
    },
];

// Initial state values
let audio = null,
    barWidth = null,
    duration = null,
    currentTime = null,
    isTimerPlaying = false,
    currentTrackIndex = 0,
    currentTrack = tracks[0];

// Set initial state values
audio = new Audio();
audio.src = currentTrack.source;
title.innerText = currentTrack.name;
singer.innerText = currentTrack.artist;

playBtn.addEventListener('click', () => {
    if (audio.paused) {
        video.play();
        isTimerPlaying = true;
    } else {
        video.pause();
        isTimerPlaying = false;
    }
});

progressBarContainer.addEventListener('click', (x) => {
    let maxduration = audio.duration;
    let position = x.pageX - progressBarContainer.offsetLeft;
    let percentage = (100 * position) / progressBarContainer.offsetWidth;
    if (percentage > 100) percentage = 100;
    if (percentage < 0) percentage = 0;
    barWidth = percentage + "%";

    audio.currentTime = (maxduration * percentage) / 100;
    progressBar.style.width = `${barWidth}%`;
    progressHead.style.setProperty("left", `${barWidth}%`);
});


skipForward.addEventListener('click', () => {

    if (currentTrackIndex < tracks.length - 1) {
        currentTrackIndex++;
    } else {
        currentTrackIndex = 0;
    }

    currentTrack = tracks[currentTrackIndex];

    audio.src = currentTrack.source;
    video.src = currentTrack.source;
    title.innerText = currentTrack.name;
    singer.innerText = currentTrack.artist;

    barWidth = 0;
    progressBar.style.width = `${barWidth}%`;
    progressHead.style.setProperty("left", `${barWidth}%`);
    currentTimeHtml.innerText = `0:00`;
    durationHtml.innerText = `0:00`;

    audio.currentTime = 0;
    audio.src = currentTrack.source;

    setTimeout(() => {
        if (isTimerPlaying) {
            video.play();
        } else {
            video.pause();
        }
    }, 300);
});

skipBack.addEventListener('click', () => {
    if (currentTrackIndex > 0) {
        currentTrackIndex--;
    } else {
        this.currentTrackIndex = this.tracks.length - 1;
    }
    currentTrack = tracks[currentTrackIndex];

    video.src = currentTrack.source;
    title.innerText = currentTrack.name;
    singer.innerText = currentTrack.artist;

    barWidth = 0;
    progressBar.style.width = `${barWidth}%`;
    progressHead.style.setProperty("left", `${barWidth}%`);
    currentTimeHtml.innerText = `0:00`;
    durationHtml.innerText = `0:00`;

    audio.currentTime = 0;
    audio.src = currentTrack.source;

    setTimeout(() => {
        if (isTimerPlaying) {
            video.play();
        } else {
            video.pause();
        }
    }, 300);
});

audio.ontimeupdate = function () {
    if (audio.duration) {
        barWidth = (100 / audio.duration) * audio.currentTime;

        let durmin = Math.floor(audio.duration / 60);
        let dursec = Math.floor(audio.duration - durmin * 60);
        let curmin = Math.floor(audio.currentTime / 60);
        let cursec = Math.floor(audio.currentTime - curmin * 60);

        if (durmin < 10) durmin = "0" + durmin;

        if (dursec < 10) dursec = "0" + dursec;

        if (curmin < 10) curmin = "0" + curmin;

        if (cursec < 10) cursec = "0" + cursec;

        duration = durmin + ":" + dursec;
        currentTime = curmin + ":" + cursec;

        progressBar.style.width = `${barWidth}%`;
        progressHead.style.setProperty("left", `${barWidth}%`)
        currentTimeHtml.innerText = `${currentTime}`;
        durationHtml.innerText = `${duration}`;

        if (isTimerPlaying) {
            playIcon.classList.remove('fa-play');
            playIcon.classList.add('fa-pause');


        } else {
            playIcon.classList.add('fa-play');
            playIcon.classList.remove('fa-pause');
        }
    }
};

audio.onended = function () { };

// Animations
// TweenMax.from('.img', 4, { rotation: "+=360", transformOrigin: "50% 50%", ease: Linear.easeNone, repeat: -1 });
// gsap.from("body, h1, .audio-img, .audio-title, .audio-singer, .audio-btns", {
//     opacity: 0,
//     duration: 2,
//     delay: 1.5,
//     y: 25,
//     ease: "expo.out",
//     stagger: 0.2,
// });
