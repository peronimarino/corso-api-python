const API_URL =
    "https://ominous-disco-gxqv9jg7xgxp3p4jq-8000.app.github.dev";

document.addEventListener(
    "DOMContentLoaded",
    () =>
    {
        controllaLogin();
        caricaMiePlaylist();
        caricaPlaylistPubbliche();
    }
);

function controllaLogin()
{
    const username =
        localStorage.getItem("username");

    if(username)
    {
        document.getElementById(
            "utenteLoggato"
        ).textContent =
            `Ciao, ${username} 👋`;
    }
}

async function caricaMiePlaylist()
{
    const token =
        localStorage.getItem("session_token");

    if(!token)
        return;

    try
    {
        const response = await fetch(
            `${API_URL}/playlist?token=${token}`
        );

        const playlist =
            await response.json();

        const contenitore =
            document.getElementById(
                "miePlaylist"
            );

        contenitore.innerHTML = "";

        playlist.forEach(item =>
        {
            contenitore.innerHTML += `
                <div class="card">

                    <h3>
                        ${item.titolo_playlist}
                    </h3>

                    <button
                        onclick="apriPlaylistPersonale(${item.id})">

                        Apri Playlist

                    </button>

                    <button
                        onclick="eliminaPlaylist(${item.id})">

                        🗑️ Elimina

                    </button>

                    <div id="personale-${item.id}">
                    </div>

                </div>
            `;
        });

    }
    catch(error)
    {
        console.error(error);
    }
}

async function caricaPlaylistPubbliche()
{
    try
    {
        const response =
            await fetch(
                `${API_URL}/playlist/pubbliche`
            );

        const playlist =
            await response.json();

        const contenitore =
            document.getElementById(
                "playlistPubbliche"
            );

        contenitore.innerHTML = "";

        playlist.forEach(item =>
        {
            contenitore.innerHTML += `
                <div class="card">

                    <h3>
                        ${item.titolo_playlist}
                    </h3>

                    <p>
                        Creata da:
                        ${item.username}
                    </p>

                    <button
                        onclick="apriPlaylistPubblica(${item.id})">

                        Apri Playlist

                    </button>

                    <div
                        id="pubblica-${item.id}">
                    </div>

                </div>
            `;
        });
    }
    catch(error)
    {
        console.error(error);
    }
}

async function creaPlaylist()
{
    const token =
        localStorage.getItem("session_token");

    const titolo =
        document.getElementById(
            "titoloPlaylist"
        ).value;

    try
    {
        const response =
            await fetch(
                `${API_URL}/playlist?token=${token}`,
                {
                    method: "POST",

                    headers:
                    {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        titolo_playlist: titolo
                    })
                }
            );

        if(response.ok)
        {
            document.getElementById(
                "titoloPlaylist"
            ).value = "";

            caricaMiePlaylist();
            caricaPlaylistPubbliche();
        }

    }
    catch(error)
    {
        console.error(error);
    }
}

async function eliminaPlaylist(id)
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    if(!confirm(
        "Vuoi eliminare la playlist?"
    ))
    {
        return;
    }

    try
    {
        await fetch(
            `${API_URL}/playlist?playlist_id=${id}&token=${token}`,
            {
                method: "DELETE"
            }
        );

        caricaMiePlaylist();
        caricaPlaylistPubbliche();

    }
    catch(error)
    {
        console.error(error);
    }
}

async function apriPlaylistPubblica(id)
{
    try
    {
        const response =
            await fetch(
            `${API_URL}/playlist/pubblica/dettaglio?playlist_id=${id}`
            );

        const film =
            await response.json();

            
        if (film.length === 0)
        {
            document.getElementById(
                `pubblica-${id}`
            ).innerHTML =
                "<p>Questa playlist è ancora vuota.</p>";

            return;
        }


        let html = "<ul>";

        film.forEach(item =>
        {
            html += `
                <li>
                    ${item.titolo}
                    (${item.anno})
                </li>
            `;
        });

        html += "</ul>";

        document.getElementById(
            `pubblica-${id}`
        ).innerHTML = html;
    }
    catch(error)
    {
        console.error(error);
    }
}

async function logout()
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    try
    {
        await fetch(
            `${API_URL}/logout?token=${token}`,
            {
                method: "POST"
            }
        );
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

    window.location.href =
        "login.html";
}

async function apriPlaylistPersonale(id)
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    try
    {
        const response =
            await fetch(
                `${API_URL}/playlist/dettaglio?playlist_id=${id}&token=${token}`
            );

        const film =
            await response.json();

        if(film.length === 0)
        {
            document.getElementById(
                `personale-${id}`
            ).innerHTML =
                "<p>Questa playlist è ancora vuota.</p>";

            return;
        }

        let html = "<ul>";

        film.forEach(item =>
        {
            html += `
                <li>

                    ${item.titolo}
                    (${item.anno})

                    <button
                        onclick="
                            rimuoviFilmPlaylist(
                                ${id},
                                ${item.id}
                            )">

                        ❌

                    </button>

                </li>
            `;
        });

        html += "</ul>";

        document.getElementById(
            `personale-${id}`
        ).innerHTML = html;
    }
    catch(error)
    {
        console.error(error);
    }
}

async function rimuoviFilmPlaylist(
    playlistId,
    filmId
)
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    const conferma =
        confirm(
            "Rimuovere il film dalla playlist?"
        );

    if(!conferma)
    {
        return;
    }

    try
    {
        await fetch(
            `${API_URL}/playlist/rimuovi-film?playlist_id=${playlistId}&film_id=${filmId}&token=${token}`,
            {
                method: "DELETE"
            }
        );

        apriPlaylistPersonale(
            playlistId
        );
    }
    catch(error)
    {
        console.error(error);

        alert(
            "Errore durante la rimozione"
        );
    }
}