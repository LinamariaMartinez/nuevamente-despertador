"""Abre la demo de NuevaMente en un navegador sin pantalla para que Streamlit Cloud no la duerma.

Si la app está dormida, pulsa el botón para despertarla y espera a que cargue.
Termina con error si la app no carga, para que se vea en rojo en GitHub Actions.
"""

import sys

from playwright.sync_api import TimeoutError as PlaywrightTimeout, sync_playwright

URL = "https://nuevamente-ia.streamlit.app/"
BOTON_DESPERTAR = "Yes, get this app back up"
ESPERA_CARGA_MS = 240_000  # la primera carga después de dormir tarda un par de minutos


def main():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto(URL, wait_until="domcontentloaded", timeout=60_000)
        pagina.wait_for_timeout(10_000)

        boton = pagina.get_by_role("button", name=BOTON_DESPERTAR)
        if boton.count():
            print("La app estaba dormida: pulsando el botón para despertarla")
            boton.first.click()
        else:
            print("La app estaba despierta")

        # La app corre dentro de un iframe; se da por cargada cuando aparece el contenido de Streamlit.
        try:
            pagina.frame_locator("iframe").first.locator("[data-testid='stApp']").wait_for(timeout=ESPERA_CARGA_MS)
        except PlaywrightTimeout:
            print("La app no terminó de cargar a tiempo", file=sys.stderr)
            navegador.close()
            return 1
        print("La app cargó")
        navegador.close()
        return 0


if __name__ == "__main__":
    sys.exit(main())
