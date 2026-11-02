# Jyoti Bhadrashetti

A responsive professional profile with separate Home, Portfolio, Résumé, Contact, and project-detail pages. Static output is in `dist/`; the content generator requires only Python’s standard library.

## Content sources

- Attached `JYOTI B_RESUME_2026 (1).pdf` is the source for professional claims, work history, education, and contact information.
- The attached portrait is used as supplied, with display-only sizing and cropping.
- The user-provided Google Drive URL points to the 2021 architecture and interiors portfolio. The Park image is extracted from page 10 (xref 657), and Parkers Restaurant from page 21 (xref 925). Both retain their original firms’ credits and are displayed separately from current Seattle work.
- Visual reference: https://www.tobymathew.com/ (Archivo headings, Raleway text, Asap subheadings, white and light gray with navy #053369).
- Dubai project descriptions, values, durations, firm credits, and images come from the earlier Drive portfolio. Additional images: Burj Residence page 19 (xref 898), Police Officers’ Club Lounge page 24 (xref 1006), Prime Medical page 26 (xref 1055), Georg Jensen page 34 (xref 1500).
- The November 2026 revision retains Archivo headings and the original colors, and uses Arial/Helvetica for more readable body text.
- The user corrected Jyoti’s title to Construction Manager throughout the site on October 31, 2026. The hosted résumé copy reflects that correction as well.

## Editing

Edit `build_site.py` for page content and project data, then run `python3 build_site.py`. Edit `dist/styles.css` for responsive styling. Navigation uses separate HTML documents and works without JavaScript. Keep résumé and displayed professional facts consistent when making updates.
