const API_URL =
    "https://ominous-disco-gxqv9jg7xgxp3p4jq-8000.app.github.dev";

document
    .getElementById("salvaFilm")
    .addEventListener(
        "click",
        aggiungiFilm
    );

async function aggiungiFilm()
{
    const token =
        localStorage.getItem(
            "session_token"
        );

    if (!token)
    {
        alert(
            "Devi effettuare il login per aggiungere un film."
        );

        return;
    }

    const titolo =
        document.getElementById(
            "titolo"
        ).value.trim();

    const trama =
        document.getElementById(
            "trama"
        ).value.trim();

    const anno =
        parseInt(
            document.getElementById(
                "anno"
            ).value
        );

    const url_locandina =
        document.getElementById(
            "locandina"
        ).value.trim();

    if (
        !titolo ||
        !trama ||
        !anno ||
        !url_locandina
    )
    {
        alert(
            "Compila tutti i campi."
        );

        return;
    }

    try
    {
        const response =
            await fetch(
                `${API_URL}/film?token=${encodeURIComponent(token)}`,
                {
                    method: "POST",

                    headers:
                    {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        titolo,
                        trama,
                        anno,
                        url_locandina
                    })
                }
            );

        const dati =
            await response.json();

        if (!response.ok)
        {
            throw new Error(
                dati.detail ||
                "Errore durante il salvataggio"
            );
        }

        alert(
            "Film aggiunto con successo!"
        );

        window.location.href =
            "catalogo.html";
    }
    catch(error)
    {
        console.error(error);

        alert(
            error.message
        );
    }
}