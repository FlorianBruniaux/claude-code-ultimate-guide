-- nocite.lua: Strip all pandoc Citation elements from the AST.
-- Replaces @key patterns (parsed as citations) with their literal text.
-- Prevents Typst "#cite(<key>)" errors when guide content contains
-- @word patterns like @Injectable, @layer, @mention outside code blocks.

function Cite(el)
  -- Return the inline content of the citation (the display text)
  -- For @key with no surrounding brackets, content is usually empty,
  -- so we reconstruct the literal @key text.
  if #el.content > 0 then
    return el.content
  end
  -- Reconstruct "@key" as plain text for bare citations
  local key = el.citations[1] and el.citations[1].id or ""
  return pandoc.Str("@" .. key)
end
