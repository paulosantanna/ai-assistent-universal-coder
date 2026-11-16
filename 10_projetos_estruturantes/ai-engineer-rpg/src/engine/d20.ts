// D20 do RPG de mesa. A rolagem é injetável para testes (e para auditoria):
// a UA fornece browserRng; testes fixam valores (21 faces cobertas por tabela).

import { D20_SIDES, D20_THRESHOLD } from './economy'

export interface Die {
  roll20: () => number // inteiro 1..20
}

export const browserRng: Die = {
  roll20: () => 1 + Math.floor(Math.random() * D20_SIDES),
}

export function isD20Success(roll: number): boolean {
  return roll >= D20_THRESHOLD
}
