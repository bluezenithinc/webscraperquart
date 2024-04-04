ELEMENTS_TO_IGNORE = [
    ############################################################
    #######   head elements
    "style",
    "script",
    "link",
    "meta",
    ############################################################
    #######   elements that are not a part of the content that we want to scrape
    "header",
    "footer",
    "nav",
    "aside",
    ############################################################
    #######   media tags
    "video",
    "audio",
    "iframe",
    "canvas",
    "svg",
    "figure",
    "picture",
    "source",
    "track",
    ############################################################
    #######   form elements
    "form",
    "input",
    "textarea",
    "button",
    "select",
    "option",
    "optgroup",
    "label",
    "fieldset",
    "legend",
    ############################################################
    #######   invisible elements
    ".hidden",
    ".hide",
    ".invisible",
    ".sr-only",
    ############################################################
    #######   elements that are divs but are actually responsible for the different role
    ".nav",
    ".navbar",
    ".sidebar",
    ".modal",
    ".popup",
    ".popup-content",
    ".header",
    ".footer",
    ".breadcrumbs",
    ".pagination",
    ############################################################
    #######   cookies
    ".cookie",
    ".cookies",
    ".cookie-banner",
    ".cookie-notice",
    "#cookie",
    "#cookies",
    ############################################################
    #######   other special cases
    ".browser-compat",
]

TAILWIND_CLASSES = {
    "h1": "text-4xl font-bold mb-4 text-gray-900 dark:text-gray-100",
    "h2": "text-3xl font-bold mb-4 text-gray-900 dark:text-gray-100",
    "h3": "text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100",
    "h4": "text-xl font-bold mb-4 text-gray-900 dark:text-gray-100",
    "h5": "text-lg font-bold mb-4 text-gray-900 dark:text-gray-100",
    "h6": "text-base font-bold mb-4 text-gray-900 dark:text-gray-100",
    "p": "text-base font-normal mb-4 break-words text-gray-900 dark:text-gray-100",
    "div": "text-base font-normal mb-4 text-gray-900 dark:text-gray-100",
    # special case for preserve_links option
    "a": {
        True: "text-blue-600 underline dark:text-blue-400",
        False: "text-gray-900 dark:text-gray-100",
    },
    "ul": "space-y-1 list-disc list-inside mb-4",
    "ol": "space-y-1 list-decimal list-inside mb-4",
    "li": "ml-4 mb-1 text-gray-900 dark:text-gray-100",
    "blockquote": "border-l-4 border-gray-300 pl-4 mb-4 italic text-gray-900 dark:text-gray-100",
    "pre": "bg-slate-100 p-4 w-full block overflow-x-auto mb-4 font-mono text-sm text-gray-800 dark:text-gray-200 dark:bg-slate-800",
    "code": "bg-slate-100 p-1 inline-block font-mono text-sm text-gray-800 dark:text-gray-200 dark:bg-slate-800",
    "table": "w-full border-collapse border-2 border-gray-300 mb-4 text-gray-900 dark:text-gray-100 dark:border-gray-700",
    "thead": "",
    "tbody": "",
    "tr": "border border-gray-300 bg-white dark:bg-slate-800",
    "th": "p-2 font-bol bg-slate-200 dark:bg-slate-700",
    "td": "p-2 border border-gray-300 dark:border-gray-700",
    "small": "text-sm",
    "strong": "font-bold",
    "em": "italic",
    "b": "font-bold",
    "i": "italic",
    "u": "underline",
    "s": "line-through",
    "del": "line-through",
    "hr": "border-gray-300 border-t-2 my-4 dark:border-gray-700",
}

DEFAULT_SCRAPING_OPTIONS = {
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "preferredLanguage": "en-US,en;q=0.9",
    "proxy": "",
    "preserveLinks": True,
    "includeImages": False,
    "ignoreCssSelectors": [],
}
