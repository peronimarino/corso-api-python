
const API_URL =
    "https://ominous-disco-gxqv9jg7xgxp3p4jq-8000.app.github.dev";



// ==========================
// RICERCA FILM
// ==========================

async function cercaFilm()
{
    const keyword =
        document.getElementById("campoRicerca").value.trim();

    const risultati =
        document.getElementById("risultati");

    risultati.innerHTML = "";

    if (!keyword)
    {
        alert("Inserisci un titolo da cercare");
        return;
    }

    try
    {
        const response = await fetch(
            `${API_URL}/film/ricerca?keyword=${encodeURIComponent(keyword)}`
        );

        if (!response.ok)
        {
            throw new Error();
        }

        const dati = await response.json();

        dati.forEach(film =>
        {
            risultati.innerHTML += `
                <div class="card">

                    <h3>${film.titolo}</h3>

                    <p>Anno: ${film.anno}</p>

                    <button onclick="apriScheda(${film.id})">
                        Apri Scheda
                    </button>

                </div>
            `;
        });
    }
    catch(error)
    {
        alert("Film non trovato");
    }
}


// ==========================
// SCHEDA FILM
// ==========================

async function apriScheda(idFilm)
{
    try
    {
        const responseFilm =
            await fetch(`${API_URL}/film/${idFilm}`);

        if (!responseFilm.ok)
        {
            throw new Error("Impossibile caricare il film");
        }

        const film =
            await responseFilm.json();

        const responseCommenti =
            await fetch(`${API_URL}/film/${idFilm}/commenti`);

        if (!responseCommenti.ok)
        {
            throw new Error("Impossibile caricare i commenti");
        }

        const commenti =
            await responseCommenti.json();

        const responseVideo =
            await fetch(`${API_URL}/film/${idFilm}/video`);

        if (!responseVideo.ok)
        {
            throw new Error("Impossibile caricare i video");
        }

        const video =
            await responseVideo.json();

        let htmlCommenti = "";

        const usernameLoggato =
    localStorage.getItem("username");

commenti.forEach(commento =>
{
    let pulsanteElimina = "";

    if(
        usernameLoggato &&
        usernameLoggato === commento.username
    )
    {
        pulsanteElimina = `
            <button
                onclick="
                    eliminaCommento(
                        ${commento.id},
                        ${idFilm}
                    )">

                🗑️ Elimina

            </button>
        `;
    }

    htmlCommenti += `
        <p>

            <strong>
                ${commento.username}
            </strong>

            <br>

            ${commento.testo}

            <br>

            ${pulsanteElimina}

        </p>
    `;
});

        if (htmlCommenti === "")
        {
            htmlCommenti =
                "<p>Nessun commento presente.</p>";
        }

        let htmlVideo = "";

video.forEach(videoItem =>
{
    const videoId =
        estraiIdYoutube(
            videoItem.url_video_youtube
        );

    const thumbnail =
        `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;

    let pulsanteElimina = "";

    if(
        usernameLoggato &&
        usernameLoggato === videoItem.username
    )
    {
        pulsanteElimina = `
            <button
                onclick="eliminaVideo(
                    ${videoItem.id},
                    ${idFilm}
                )">

                🗑️ Elimina

            </button>
        `;
    }

    htmlVideo += `

        <div class="videoCard">

            <img
            class="thumbnailYoutube"
            src="${thumbnail}"
            alt="Thumbnail del video">

            <p>

                <strong>
                    ${videoItem.username}
                </strong>

            </p>

            <p>

                ${videoItem.commento}

            </p>

            <a href="${videoItem.url_video_youtube}" target="_blank" rel="noopener noreferrer">
                🎥 Guarda su Youtube
            </a>

            <br><br>

            ${pulsanteElimina}

        </div>

    `;
});

        if (htmlVideo === "")
        {
            htmlVideo = "<p>Nessun video presente.</p>";
        }
        let pulsanteEliminaFilm = "";

        if(film.utente_id)
        {
            pulsanteEliminaFilm = `
                <button
                    onclick="eliminaFilm(${film.id})">

                    🗑️ Elimina Film

                </button>
            `;
        }
        const scheda =
            document.getElementById("schedaFilm");

        scheda.innerHTML = `
            <h2>${film.titolo}</h2>
            ${pulsanteEliminaFilm}
            <img class="locandina" src="${film.url_locandina}" alt="${film.titolo}">
            <p><strong>Anno:</strong> ${film.anno}</p>
            <p>${film.trama}</p>
            <div class="sezione">
                <h3>Video della Community</h3>
                ${htmlVideo}
                <div id="areaVideo"></div>
            </div>
            <div class="sezione">
                <h3>Commenti</h3>
                ${htmlCommenti}
                <div id="areaCommento"></div>
            </div>
            <div class="sezione">

            <h3>Playlist</h3>

            <div id="areaPlaylist"></div>

            </div>
        `;

        scheda.style.display = "block";

        const token =
            localStorage.getItem("session_token");

        if (token)
        {
            const areaCommento = document.getElementById("areaCommento");
            if (areaCommento)
            {
                areaCommento.innerHTML = `
                    <h4>Nuovo Commento</h4>
                    <textarea id="testoCommento" placeholder="Scrivi il tuo commento..."></textarea>
                    <br>
                    <button onclick="pubblicaCommento(${idFilm})">Pubblica Commento</button>
                `;
            }

            const areaVideo = document.getElementById("areaVideo");
            if (areaVideo)
            {
                areaVideo.innerHTML = `
                    <h4>Aggiungi Video</h4>
                    <input type="text" id="urlVideo" placeholder="https://youtu.be/...">
                    <br><br>
                    <textarea id="commentoVideo" placeholder="Commento al video"></textarea>
                    <br>
                    <button onclick="pubblicaVideo(${idFilm})">Pubblica Video</button>
                `;
            }
            const areaPlaylist =document.getElementById("areaPlaylist");

            if(areaPlaylist)
            {
                caricaPlaylistUtente(idFilm);
            }
        }

        scheda.scrollIntoView({
            behavior: "smooth"
        });
    }
    catch(error)
    {
        console.error(error);

        alert(
            "Errore durante il caricamento del film"
        );
    }
}


// ==========================
// CONTROLLO LOGIN
// ==========================


document.addEventListener(
    "DOMContentLoaded",
    controllaLogin
);

function controllaLogin()
{

    document.getElementById(
    "nuovoFilmLink"
    ).style.display = "none";


    const token =
        localStorage.getItem("session_token");

    const username =
        localStorage.getItem("username");

    if (token && username)
    {

        document.getElementById(
            "nuovoFilmLink"
        ).style.display ="inline-block";
        
        document.getElementById(
            "utenteLoggato"
        ).textContent =
            `Ciao, ${username} 👋`;

        document.getElementById(
            "logoutBtn"
        ).style.display =
            "inline-block";

        document.getElementById(
            "loginLink"
        ).style.display =
            "none";

        document.getElementById(
            "registerLink"
        ).style.display =
            "none";
    }
}


// ==========================
// LOGOUT
// ==========================

async function logout()
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    try
    {
        if (token)
        {
            await fetch(
                `${API_URL}/logout?token=${encodeURIComponent(token)}`,
                {
                    method: "POST"
                }
            );
        }
    }
    catch(error)
    {
        console.error(error);
    }

    localStorage.removeItem(
        "session_token"
    );

    localStorage.removeItem(
        "username"
    );

    alert("Logout effettuato");

    window.location.reload();
}

async function pubblicaCommento(idFilm)
{
    const token =
        localStorage.getItem("session_token");

    if (!token)
    {
        alert("Devi essere loggato per pubblicare un commento");
        return;
    }

    const testo =
        document.getElementById(
            "testoCommento"
        ).value.trim();

    if(!testo)
    {
        alert(
            "Inserisci un commento"
        );

        return;
    }

    try
    {
        const response =
            await fetch(
                `${API_URL}/film/${idFilm}/commento?token=${encodeURIComponent(token)}`,
                {
                    method: "POST",

                    headers:
                    {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        testo: testo
                    })
                }
            );

        if(!response.ok)
        {
            throw new Error();
        }

        alert(
            "Commento pubblicato!"
        );

        apriScheda(idFilm);
    }
    catch(error)
    {
        console.error(error);

        alert(
            "Errore durante l'inserimento del commento"
        );
    }
}

async function pubblicaVideo(idFilm)
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    if (!token)
    {
        alert("Devi effettuare il login per pubblicare un video");
        return;
    }

    const urlVideo =
        document.getElementById(
            "urlVideo"
        ).value.trim();

    const commento =
        document.getElementById(
            "commentoVideo"
        ).value.trim();

    if(!urlVideo)
    {
        alert(
            "Inserisci l'URL del video"
        );

        return;
    }

    try
    {
        const response =
            await fetch(
                `${API_URL}/film/${idFilm}/video?token=${encodeURIComponent(token)}`,
                {
                    method: "POST",

                    headers:
                    {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        url_video_youtube: urlVideo,
                        commento: commento
                    })
                }
            );

        if(!response.ok)
        {
            throw new Error();
        }

        alert("Video pubblicato!");

        apriScheda(idFilm);
    }
    catch(error)
    {
        console.error(error);

        alert(
            "Errore durante la pubblicazione del video"
        );
    }
}

function estraiIdYoutube(url)
{
    if(url.includes("youtu.be/"))
    {
        return url.split("youtu.be/")[1].split("?")[0];
    }

    if(url.includes("watch?v="))
    {
        return url.split("watch?v=")[1].split("&")[0];
    }

    return null;
}
async function eliminaCommento(
    commentoId,
    filmId
)
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    const conferma =
        confirm(
            "Eliminare il commento?"
        );

    if(!conferma)
    {
        return;
    }

    try
    {
        await fetch(
            `${API_URL}/film/commento?commento_id=${commentoId}&token=${token}`,
            {
                method: "DELETE"
            }
        );

        apriScheda(filmId);
    }
    catch(error)
    {
        console.error(error);

        alert(
            "Errore durante l'eliminazione"
        );
    }
}

async function eliminaVideo(
    videoId,
    filmId
)
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    const conferma =
        confirm(
            "Eliminare il video?"
        );

    if(!conferma)
    {
        return;
    }

    try
    {
        await fetch(
            `${API_URL}/film/video?video_id=${videoId}&token=${token}`,
            {
                method: "DELETE"
            }
        );

        apriScheda(filmId);
    }
    catch(error)
    {
        console.error(error);

        alert(
            "Errore durante l'eliminazione del video"
        );
    }
}
async function caricaPlaylistUtente(idFilm)
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    try
    {
        const response =
            await fetch(
                `${API_URL}/playlist?token=${token}`
            );

        const playlist =
            await response.json();

        let options = "";

        playlist.forEach(item =>
        {
            options += `
                <option value="${item.id}">
                    ${item.titolo_playlist}
                </option>
            `;
        });

        document.getElementById(
            "areaPlaylist"
        ).innerHTML = `

            <h4>
                Aggiungi alla Playlist
            </h4>

            <select id="playlistSelect">

                ${options}

            </select>

            <button
                onclick="aggiungiFilmPlaylist(${idFilm})">

                ➕ Aggiungi

            </button>

        `;
    }
    catch(error)
    {
        console.error(error);
    }
}

async function aggiungiFilmPlaylist(idFilm)
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    const playlistId =
        document.getElementById(
            "playlistSelect"
        ).value;

    try
    {
        const response =
            await fetch(
                `${API_URL}/playlist/aggiungi-film?playlist_id=${playlistId}&film_id=${idFilm}&token=${token}`,
                {
                    method: "POST"
                }
            );

        const dati =
            await response.json();

        if(!response.ok)
        {
            throw new Error(
                dati.detail || "Errore"
            );
        }

        alert(
            "Film aggiunto alla playlist!"
        );
    }
    catch(error)
    {
        console.error(error);

        alert(
            "Errore durante l'aggiunta del film"
        );
    }
}

async function eliminaFilm(filmId)
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    const conferma =
        confirm(
            "Vuoi eliminare questo film?"
        );

    if(!conferma)
    {
        return;
    }

    try
    {
        const response =
            await fetch(
                `${API_URL}/film?film_id=${filmId}&token=${token}`,
                {
                    method: "DELETE"
                }
            );

        const dati =
            await response.json();

        if(!response.ok)
        {
            throw new Error(
                dati.detail ||
                "Errore durante l'eliminazione"
            );
        }

        alert(
            "Film eliminato con successo!"
        );

        document.getElementById(
            "schedaFilm"
        ).style.display = "none";

        document.getElementById(
            "risultati"
        ).innerHTML = "";

    }
    catch(error)
    {
        console.error(error);

        alert(
            error.message
        );
    }
}