-- fix-lists.lua
-- Unified list fix for Typst/whitepaper rendering.
--
-- Problem 1: Tight list items (Plain blocks) are inlined into the
--   preceding paragraph by the Typst writer → "text: - item1 - item2"
--   Fix: convert Plain → Para in all BulletList/OrderedList items.
--
-- Problem 2: Task list items render as "• ☐ text" (two markers).
--   Pandoc converts - [ ] → ☐ (U+2610) and - [x] → ☒ (U+2612) Str nodes.
--   Fix: replace ☐/☒ with styled Typst raw inline boxes, remove the Str.

local UNCHECKED = "\xE2\x98\x90"  -- UTF-8 for ☐ (U+2610)
local CHECKED   = "\xE2\x98\x92"  -- UTF-8 for ☒ (U+2612)

-- Typst raw content for styled checkboxes (Bold Guy palette)
local BOX_UNCHECKED = '#box(width:0.85em,height:0.85em,stroke:0.6pt+rgb("#6b6053"),radius:2pt,inset:0pt)[]'
local BOX_CHECKED   = '#box(width:0.85em,height:0.85em,stroke:0.6pt+rgb("#d4520a"),fill:rgb("#d4520a"),radius:2pt,inset:(x:1pt,y:1pt))[#align(center+horizon)[#text(size:6pt,fill:white,weight:"bold")[\u{2713}]]]'

local function fix_item(item)
  local new_blocks = {}
  for _, block in ipairs(item) do
    local inlines = nil
    local is_plain = block.t == "Plain"
    local is_para  = block.t == "Para"

    if is_plain or is_para then
      inlines = block.c
      local first = inlines[1]

      -- Detect task list checkbox as first inline
      if first and first.t == "Str" and
         (first.c == UNCHECKED or first.c == CHECKED) then
        local checked = first.c == CHECKED
        local box_raw = pandoc.RawInline("typst", checked and BOX_CHECKED or BOX_UNCHECKED)

        -- Build new inline list: styled box + space + rest of content (skip ☐ + Space)
        local new_inlines = { box_raw }
        local start = 2
        if inlines[start] and inlines[start].t == "Space" then
          start = start + 1
        end
        for i = start, #inlines do
          table.insert(new_inlines, inlines[i])
        end
        -- Always Para (not Plain) so it renders as a block
        table.insert(new_blocks, pandoc.Para(new_inlines))
      else
        -- Regular item: convert Plain → Para to prevent inline merging
        if is_plain then
          table.insert(new_blocks, pandoc.Para(inlines))
        else
          table.insert(new_blocks, block)
        end
      end
    else
      table.insert(new_blocks, block)
    end
  end
  return new_blocks
end

local function fix_items(items)
  local result = {}
  for _, item in ipairs(items) do
    table.insert(result, fix_item(item))
  end
  return result
end

function BulletList(el)
  return pandoc.BulletList(fix_items(el.content))
end

function OrderedList(el)
  return pandoc.OrderedList(fix_items(el.content), el.listAttributes)
end
