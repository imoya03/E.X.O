async function cargarComponentes() {
  // 1. Detectar en qué carpeta estamos
  const estamosEnPages = window.location.pathname.includes("/pages/");
  const rutaComponentes = estamosEnPages ? "" : "pages/";

  try {
    // 2. Cargar Header y Footer
    const headerRes = await fetch(rutaComponentes + "header.html");
    document.getElementById("header-placeholder").outerHTML =
      await headerRes.text();

    const footerRes = await fetch(rutaComponentes + "footer.html");
    document.getElementById("footer-placeholder").outerHTML =
      await footerRes.text();

    // 3. Ajustar rutas de los enlaces del menú
    document.querySelectorAll("#header a, #menu a").forEach((enlace) => {
      let href = enlace.getAttribute("href");
      if (!href || href.startsWith("#") || href.startsWith("http")) return;

      if (!estamosEnPages) {
        if (href !== "index.html" && !href.startsWith("pages/")) {
          enlace.setAttribute("href", "pages/" + href);
        }
      } else {
        if (href === "index.html") {
          enlace.setAttribute("href", "../index.html");
        }
      }
    });

    // 4. Internacionalización
    if (typeof window.iniciarIdiomas === "function") {
      window.iniciarIdiomas();
    }

    // 5. Cargar main.js y forzar la activación de la plantilla
    const rutaAssets = estamosEnPages ? "../assets/" : "assets/";
    const script = document.createElement("script");
    script.src = rutaAssets + "js/main.js";

    // MAGIA AQUÍ: Cuando main.js cargue, obligamos a jQuery y a la página a activar los estilos
    script.onload = function () {
      // Quitar el estado de precarga
      document.body.classList.remove("is-preload");

      // Notificar a jQuery que la página está lista para que ordene la posición del header
      if (typeof jQuery !== "undefined") {
        jQuery(window).trigger("load");
      }
    };

    document.body.appendChild(script);
  } catch (error) {
    console.error("Error cargando componentes:", error);
    document.body.classList.remove("is-preload");
  }
}

// Controlar la ejecución del script independientemente de cuándo lea la página
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", cargarComponentes);
} else {
  cargarComponentes();
}
