# APPM 5630 Final Project

- The project is due at the beginning of the final exam time (in 2025, this was 7:30 PM May 3rd)
- The project consists of a 5-10 minute presentation and a short paper. There is no strict length requirement for the paper, but aim for 4 to 6 pages single-spaced (including figures). Paper lengths are a guideline, as I’m aware you can add figures, code, adjust white space and font to make it longer/shorter.
  - If you submit a 15-20 (or longer) page single-spaced paper, I will not be able to read all of it in detail.  We typically have 12+ groups, and so I don't have the time read that much math
  - Conversely, a 5 page *double-spaced* paper is likely too short to demonstrate your knowledge and the subject content.
- If you really wanted to, you could write a longer, much more detailed paper and skip the presentation. This isn't so much about adding length as it is adding careful analysis.
- You are encouraged to form groups; group sizes can be 1 (single person), 2 or 3. No larger please.
- By the last day of class, email me to let me know your group (or signup on the spreadsheet that I mention in Canvas), so I know how many groups there are; this will help me schedule the presentations.
- The project is 20% of your overall class grade. It cannot be dropped.
- Deliverables:
  - Written paper (typeset; Latex is suggested but not required), turned in via Canvas
  - 5 - 10 minute talk; exact time length will depend on how many groups w have
  - Slides for the talk (turned in via Canvas or emailed directly to instructor)
- More details:
  - Class participation is extra important these days, as a sign of respect to your fellow students.  You lose 10% of your project grade if you do not attend presentations (unless you have a valid reason and contacted me about it).
  - You also lose 10% of your project grade if you are not ready to present on the day when you're scheduled to speak
## What is a valid project?
- The project can be theoretical or computational (or both)
- One option is a "traditional" class-project, where you investigate an idea, and/or run simulations or do derivations or proofs, and/or connect several different ideas (e.g., create new ideas, though the originality/impact obviously does not have to rise to the level of a journal publication);
- You're encouraged to pursue an area related to your research interests
- Specific journal articles are a good starting point
  - You can reproduce their results
  - You can compare several methods
  - You can apply a method to a new problem or area
  - You can tweak a method
  - You can redo theoretical derivations more clearly (or with more details)
  - You can do a "book-report style"”" analysis of a paper, critical evaluating it (think of it as a peer-review for an article)
- Your results do not have to be novel; you do not need to write a journal quality paper!
- You'll want to related your project to something you learned in the class (see Rubric #2)
- Non-convex problems are valid topics *sometimes*, since a lot of convex optimization is linked to non-convex optimization
  - e.g. non-linear programming (NLP) solvers are used for both convex optimization (to find a global minimizer) and non-convex optimization (to find a stationary point). So you project could be about a NLP algorithm
  - e.g. convex relaxations of non-convex problems
  - I would prefer that you do **not** do a project that is focused only on an inherently non-convex idea, e.g., combinatorial optimization. But you could tackle, for example, integer linear programming if your focus is on the convex relaxations used in a branch-and-bound method.
- When in doubt about whether a project idea is valid, you can always email the instructor and ask!

### Some project ideas
- Manifold optimization is always popular. Start with [an introduction to Optimization on smooth manifolds](https://www.nicolasboumal.net/book/) by Nicolas Boumal (Cambridge University Press, 2023)
- Look at automated convergence analysis via the "PEP" framework. Start with [PEPit: Performance Estimation in Python](https://pepit.readthedocs.io/en/0.3.2/#) and read their related docs and papers
- Optimization in infinite dimensions; and when you can convert this to finite dimensional equivalent problems.
See Corollary 3.1 in [Towards a Mathematical Theory of Super-Resolution](https://math.nyu.edu/~cfgranda/pages/stuff/super-res.pdf) (E. Candès and C. Fernandez-Granda, in *Comm. Pure Appl. Math.*, 2013), or B. Dumitrescu, *Positive trigonometric polynomials and signal processing applications* (Springer, 2007) for more complete background.


## Rubric
Because the type of report is a bit open-ended, the rubric below is necessarily a bit vague:
1. Valid/interesting project (25%), and point of project is clear. For example, for an independent investigation, the problem you are trying to solve is explained and motivated and non-trivial. For a book-report style project, presenting on a paper, you need some kind of thesis (e.g., “This paper shows the power of this approach...”) and not just a summary, and explain why you chose that paper. For reproducing the results of a paper (computationally or analytically by going through a proof in extra detail), explain why you chose the paper, and why you are interested in their results (are they amazing results? do you distrust them? do they nicely illustrate concepts from class)?

2. Relate the project to a concept from class (25%). **Your project must include a paragraph describing how it involves concepts learned in class.**

3. Insightful discussion (25%). You should discuss/analyze your results, and/or validate a conclusion. For a paper review, you should discuss the strengths and weaknesses of the paper. For a project that involves generating your own results, the quality of the actual work is included in this category.

4. Professional communication (25%) of the written document and the oral presentation (and the slides). Well-organized and precise communication, grammatically correct writing, nicely format- ted documents and figures. Figures should be labeled appropriately. For the talk, the standard we're judging against is: "is information conveyed?"

Here is a [more detailed rubric](ProjectRubric.pdf) that I will actually use for grading the projects.

## Tips on giving the talk
- The length of the talk will depend on how many groups we have, but typically it's 5 to 10 minutes. Don't go over time!
- A rule-of-thumb for slides is 1 slide per minute (not counting overlays). You don't have to follow this strictly, but you certainly don't want to have 20 slides for a 10 minute talk (even if they are just pictures/figures)
- Don't feel compelled to speak about all the details of your project. Given the time limit and the limits of your audience's attention span, you may need to focus on just the key part.  Less is more here.
- For figures, it's common practice to copy figures you made for a written report/article
  - However, in many cases it would be better to redo the figures and simplify them. For example, in the paper, you can have a plot showing a half dozen competing methods. For the presentation, only show the top 1 or 2 competing methods.
  - When coding, keep in mind that you will likely want to make several variations of your plot, so make the plotting code with that in mind. You'll try out a few versions to see what you like best for your draft (e.g., log-scale?); then you'll create other versions for a presentation; and for a paper, you'll create more versions for the revision in order to appease reviewers; and also for a paper, you might speak about this method 10 years down the road in a summary talk, and want a really simplified version for that. So, make sure you can recreate the plot easily. In Matlab, save the `.fig` file, which you can open and edit manually if needed. (And for papers, share the plotting code with all co-authors, since they might make their own variations for their own talks; if the code is small, put it on overleaf alongside the LaTeX files!)
- Practice! Especially if you're nervous. The best antidote to nerves is to overpractice. You can even practice in the same room (just come in late one evening)
- Look at your audience as much as possible. Move around, stay dynamic.  If you want to point at something on the slide, better to do it physically (with your arm, or a laser pointer) rather than use the mouse cursor
  - Keep arms out of pockets
  - No gum
- Don't read from a prepared script!
  - The only exceptions are if you are not a native English speaker and very worried about your English proficiency, and/or if you are excessively nervous. In those cases you could memorize the talk, but only as a temporary fix. You'll eventually need to learn to give talks that are not memorized.
- Don't look at physical notes. If you really need notes, then use Keynote or Powerpoint (rather than PDFs) with their presenter feature so that you can see presenter notes. But these notes should be very short, like 4 bullet points (one sentence each) per slide.
  - At professional conferences, most speakers do not use presenter notes
  - Instead, practice the talk enough times so that you remember what the key points to mention on each slide are (but don't **memorize** it word-for-word)
- Introduce yourself! It can be brief, but at least your name and your role at the university. You can also use this time to preview where the talk is going
- To help you prepare for your talk, you could ask yourself: what are the learning outcomes for the audience?
  - What are the key things you want the audience to know after listening to your talk?
  - Generally, this should be 3 (or fewer) high-level things
  - Obviously, this would change with a job talk, or thesis defense, or a keynote talk, etc.
- Professors (and the internet) don't agree 100% on what makes an excellent talk
  - But most of us agree about most things.
  - So, take a look at other internet resources about what makes a good talk.  Use your judgment of course...

  ## Common issues in written reports
  These are just some common issues I see over-and-over:
  - In LaTeX, left quotes are written with two backticks; see [here for info](https://www.maths.tcd.ie/~dwilkins/LaTeXPrimer/QuotDash.html). Using the normal quite mark on your keyboard for left quotes makes them face the wrong way.
  - in LaTex, after a displayed equation (that is, after using `$$` or `\[ ... \]` or `\begin{equation}...\end{equation`}):
    - don't forget to punctuation like you would a normal sentence, and do that before the displayed environment ends (see [12.4.5 in SIAM style guide](https://epubs.siam.org/pb-assets/files/SIAM_STYLE_GUIDE_2019.pdf))
    - if continuing the paragraph afterward, so that you do not want to indent the new line, then don't allow a blank line after the equation otherwise it will add the indent for you.
  - All images in figures should be a [vector graphics format](https://en.wikipedia.org/wiki/Vector_graphics) like PDF (or SVG or PS/EPS, or generated by tikz, etc.) rather than a raster graphics format like JPEG/PNG/GIF.  PDFs can include raster graphics, but they will treat text as a font. Most modern fonts are vector fonts like the class of PostScript Type 1 fonts (an exception are old latex documents that used bitmapped fonts), so this means that you can zoom in on a figure and the text still looks nice
  - Almost all beginning scientific writers make their figures too small.  The font size in your figure should be similar to the font size in the main text (though usually it's not necessary to make it exactly the same unless you are OCD).
  - Don't mix-and-match tenses (past vs future). It doens't really matter what you use but keep it consistent
    - Also keep English spelling/dialects consistent, i.e., choose "center" (American) or "centre" (British, Indian), or "optimize" or "optimise", but don't mix-and-match.
  - Don't make it too informal; avoid "I" and "you"; avoid a narrative of your process.  On the other hand, don't try too hard to make it sound "scientific", just aim for natural and to-the-point.  Edit it, and as you do so, make it shorter.
    - Some people recommend passive voice to avoid "we" pronouns. My personal opinion is that passive voice should be avoided when possible, and that "we" isn't an issue in formal writing.  Often you can write a better phrasing that is avoids both passive voice **and** "we".  e.g., "We analyzed the data..." ("we" phrasing) or "The data were analyzed..." (passive voice) are both so-so; try something like "The data in Figure 3 show that ..."
  - In bibtex, for the titles of papers, only the first letter of the first word is capitalized by default. If you want to capitalize something (a proper name or acronym) then surround it by { ... } brackets. See [the internet](https://tex.stackexchange.com/a/10775/4603) for more details; you can also learn more than you need to about font kerning...