// typst-show.typ - Bridge Quarto metadata to whitepaper template

// Import cheatsheet components so they're available in whitepaper-typst documents
#import "_extensions/whitepaper/cheatsheet-template.typ": context-bar, do-dont, golden-rules, fiche-recap

#show: doc => whitepaper(
  title: "$title$",
  $if(subtitle)$
  subtitle: "$subtitle$",
  $endif$
  $if(by-author)$
  author: "$for(by-author)$$by-author.name.literal$$sep$, $endfor$",
  $endif$
  $if(date)$
  date: "$date$",
  $endif$
  $if(lang)$
  lang: "$lang$",
  $endif$
  $if(region)$
  region: "$region$",
  $endif$
  $if(abstract)$
  abstract: [$abstract$],
  $endif$
  $if(margin)$
  margin: ($for(margin/pairs)$$margin.key$: $margin.value$,$endfor$),
  $endif$
  $if(papersize)$
  paper: "$papersize$",
  $endif$
  $if(mainfont)$
  font: ("$mainfont$",),
  $endif$
  $if(fontsize)$
  fontsize: $fontsize$,
  $endif$
  $if(section-numbering)$
  sectionnumbering: "$section-numbering$",
  $endif$
  $if(toc)$
  toc: $toc$,
  $endif$
  $if(toc-title)$
  toc_title: "$toc-title$",
  $endif$
  $if(toc-depth)$
  toc_depth: $toc-depth$,
  $endif$
  $if(version)$
  version: "$version$",
  $endif$
  $if(wp-version)$
  wp-version: "$wp-version$",
  $endif$
  $if(series)$
  series: "$series$",
  $endif$
  cols: $if(columns)$$columns$$else$1$endif$,
  doc,
)
