// Recap Card Show - Bridge between Quarto and Typst template
// Note: recap-card() is defined in typst-template.typ (concatenated by Quarto before this file)

#show: recap-card.with(
$if(title)$
  title: "$title$",
$endif$
$if(subtitle)$
  subtitle: "$subtitle$",
$endif$
$if(card-number)$
  card-number: "$card-number$",
$endif$
$if(category)$
  category: "$category$",
$endif$
$if(difficulty)$
  difficulty: "$difficulty$",
$endif$
$if(author)$
  author: "$author$",
$endif$
$if(version)$
  version: "$version$",
$endif$
$if(date)$
  date: "$date$",
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
$if(layout)$
  layout: "$layout$",
$endif$
)
