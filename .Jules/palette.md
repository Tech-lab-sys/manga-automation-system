## 2024-06-27 - Enhance Jinja2 Form Generation Accessibility
**Learning:** For server-rendered forms (like FastAPI returning Jinja templates) that process long-running tasks synchronously without Javascript frameworks, a simple vanilla JS `onsubmit` handler disabling the submit button and showing a spinner prevents double-submissions. Furthermore, adding dynamic `role="alert"` (for errors) and `role="status"` (for success) around Jinja blocks ensures screen readers immediately announce the newly rendered page results after a postback.
**Action:** Always include inline JS loading states for long-running synchronous form submits and wrap Jinja conditional feedback blocks in appropriate ARIA live region roles to improve the UX and accessibility.

## 2026-06-27 - Tailwind Focus Ring Visibility
**Learning:** In Tailwind CSS, simply adding a color utility like `focus:ring-indigo-500` will not render a focus ring unless a ring width utility like `focus:ring` or `focus:ring-2` is also applied. This can unintentionally create inaccessible inputs with no visible keyboard focus indicator despite the presence of the color utility.
**Action:** Always ensure both ring width (`focus:ring-2`) and color utilities are paired when building custom inputs to guarantee focus visibility for keyboard accessibility, and remove default browser outlines with `focus:outline-none`.
