-- Markdown separator lengths are not layout constraints for narrow cards.
-- Let Typst allocate columns from their content instead of inherited ratios.
function Table(element)
  if FORMAT:match("typst") then
    for index, column in ipairs(element.colspecs) do
      element.colspecs[index] = {column[1], nil}
    end
  end
  return element
end
