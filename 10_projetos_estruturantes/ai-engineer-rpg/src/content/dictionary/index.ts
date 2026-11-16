// Mesclador dos fragmentos de dicionário por reino: fórmula central e exemplo
// prático de cada termo. O glossário final (src/content/glossary.ts) casa cada
// termo pelo id — os fragmentos não se sobrepõem entre reinos.

import { realm0Fill } from './realm0'
import { realm1Fill } from './realm1'
import { realm2Fill } from './realm2'
import { realm3Fill } from './realm3'
import { realm4Fill } from './realm4'
import { realm5Fill } from './realm5'
import { realm6Fill } from './realm6'

export const dictionaryFill: Record<string, { formula: string; example: string }> = {
  ...realm0Fill,
  ...realm1Fill,
  ...realm2Fill,
  ...realm3Fill,
  ...realm4Fill,
  ...realm5Fill,
  ...realm6Fill,
}
