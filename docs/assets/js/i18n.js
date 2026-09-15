(function () {
  "use strict";

  const availableLanguages = ["es", "en"];
  const defaultLanguage = "es";

  const languageNames = {
    es: "ES",
    en: "EN",
    fr: "FR",
    de: "DE",
    pt: "PT",
    it: "IT",
  };

  let currentLanguage = null;

  function getNestedValue(object, path) {
    return path.split(".").reduce(function (current, key) {
      return current ? current[key] : undefined;
    }, object);
  }

  function updateLanguageButton() {
    // Lo buscamos dinámicamente cada vez que se necesite
    const langToggle = document.getElementById("lang-toggle");
    if (!langToggle || availableLanguages.length < 2) return;

    const currentIndex = availableLanguages.indexOf(currentLanguage);
    const nextIndex = (currentIndex + 1) % availableLanguages.length;
    const nextLanguage = availableLanguages[nextIndex];

    langToggle.textContent =
      languageNames[nextLanguage] || nextLanguage.toUpperCase();
    langToggle.setAttribute(
      "aria-label",
      `Cambiar idioma a ${nextLanguage.toUpperCase()}`,
    );
  }

  function applyTranslations(translations) {
    document.querySelectorAll("[data-i18n]").forEach(function (element) {
      const key = element.getAttribute("data-i18n");
      const translation = getNestedValue(translations, key);
      if (translation !== undefined) {
        element.textContent = translation;
      }
    });

    document
      .querySelectorAll("[data-i18n-placeholder]")
      .forEach(function (element) {
        const key = element.getAttribute("data-i18n-placeholder");
        const translation = getNestedValue(translations, key);
        if (translation !== undefined) {
          element.placeholder = translation;
        }
      });

    document.querySelectorAll("[data-i18n-value]").forEach(function (element) {
      const key = element.getAttribute("data-i18n-value");
      const translation = getNestedValue(translations, key);
      if (translation !== undefined) {
        element.value = translation;
      }
    });
  }

  async function loadLanguage(language) {
    try {
      // Arreglo mágico: Si estamos en /pages/, subimos un nivel para buscar /locales/
      const estamosEnPages = window.location.pathname.includes("/pages/");
      const rutaLocales = estamosEnPages ? "../locales/" : "locales/";

      const response = await fetch(`${rutaLocales}${language}.json`);

      if (!response.ok) {
        throw new Error(`No se encontró ${rutaLocales}${language}.json`);
      }

      const translations = await response.json();
      applyTranslations(translations);

      currentLanguage = language;
      document.documentElement.lang = language;
      localStorage.setItem("language", language);

      updateLanguageButton();
    } catch (error) {
      console.error("Error al cargar el idioma:", error);
    }
  }

  function getInitialLanguage() {
    const savedLanguage = localStorage.getItem("language");
    if (savedLanguage && availableLanguages.includes(savedLanguage)) {
      return savedLanguage;
    }

    const browserLanguage = navigator.language
      ? navigator.language.substring(0, 2)
      : defaultLanguage;
    return availableLanguages.includes(browserLanguage)
      ? browserLanguage
      : defaultLanguage;
  }

  // ==========================================
  // EXPORTAMOS LA FUNCIÓN AL MUNDO EXTERIOR
  // ==========================================
  window.iniciarIdiomas = function () {
    // 1. Cargamos el idioma (esto traducirá el header y footer recién inyectados)
    loadLanguage(currentLanguage || getInitialLanguage());

    // 2. Buscamos el botón AHORA que ya existe y le ponemos el evento del clic
    const langToggle = document.getElementById("lang-toggle");
    if (langToggle) {
      // Removemos eventos previos por si acaso para evitar clics dobles
      const nuevoBoton = langToggle.cloneNode(true);
      langToggle.parentNode.replaceChild(nuevoBoton, langToggle);

      nuevoBoton.addEventListener("click", function (event) {
        event.preventDefault();
        if (availableLanguages.length < 2) return;

        const currentIndex = availableLanguages.indexOf(currentLanguage);
        const nextIndex = (currentIndex + 1) % availableLanguages.length;
        const nextLanguage = availableLanguages[nextIndex];

        loadLanguage(nextLanguage);
      });
    }
  };

  // Inicializamos la primera vez (para el index o contenido estático)
  window.iniciarIdiomas();
})();
