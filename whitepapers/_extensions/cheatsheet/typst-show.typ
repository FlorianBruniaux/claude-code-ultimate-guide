// Cheatsheet Show - Bridge between Quarto and Typst template

#show: cheatsheet.with(
$if(title)$
  title: [$title$],
$endif$
$if(subtitle)$
  subtitle: [$subtitle$],
$endif$
$if(author)$
  author: [$author$],
$endif$
$if(date)$
  date: [$date$],
$endif$
$if(version)$
  version: "$version$",
$endif$
$if(series)$
  series: "$series$",
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
$if(fontsize)$
  fontsize: $fontsize$,
$endif$
)
