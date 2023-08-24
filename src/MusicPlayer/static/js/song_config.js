let audioNL = document.querySelectorAll('audio');
let audio = Array.apply(null, audioNL);

audio.forEach(t => {
    let index = audio.indexOf(t);

    t.addEventListener('play', () => {
        audio.forEach(subT => {
            subT !== audio[index] ?
            (subT.pause(), subT.currentTime = 0) : 
            subT.play()
        })
    })
    t.addEventListener('play', ()=> {})
});