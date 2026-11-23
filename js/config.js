// ============================================================
//  SITE SETTINGS  (T. Roy: this is the only file you edit)
// ============================================================

// The same Google Apps Script web app link as the maths site.
// Leave it empty ("") and scores are only saved in the browser.
const SHEET_URL = "https://script.google.com/macros/s/AKfycbwVtMPLi4H1VjIQ4dFfTXrE6Pg900o2RGuvnM8ijyLJJeFtSkepXLhJdVzUA8olowu9/exec";

const SUBJECT = "English";   // English scores go to the "English Scores" tab
const CLASS = "6/1";         // this site is for class 6/1 only
const CLASSES = [CLASS];

// Units shown on the home page. "ready: true" means the data file exists.
const UNITS = [
  { id: "05", title: "Exciting Sports",      pages: "Book p.50 to 59 · Workbook p.40 to 47", icon: "🏄", ready: true  },
  { id: "06", title: "History's a Mystery",  pages: "Book p.60 to 69 · Workbook p.48 to 55", icon: "🏛️", ready: true  },
  { id: "07", title: "Chocolate!",           pages: "Book p.70 to 79 · Workbook p.56 to 63", icon: "🍫", ready: true  },
  { id: "08", title: "Cool Vacations!",      pages: "Book p.80 to 89 · Workbook p.64 to 71", icon: "🏖️", ready: true  }
];
const EXTRAS = [
  { id: "review", title: "Review and Let's Talk", icon: "⭐", ready: false },
  { id: "verbs",  title: "Irregular Verbs",       icon: "📚", ready: false }
];
