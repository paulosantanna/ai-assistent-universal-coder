import { describe, expect, it } from 'vitest'
import { isD20Success } from '../src/engine/d20'

describe('D20: limiar do usuário (>= 15 acerta)', () => {
  const rolls: Array<[number, boolean]> = [
    [1, false], [5, false], [10, false], [14, false],
    [15, true], [16, true], [19, true], [20, true],
  ]
  for (const [roll, success] of rolls) {
    it(`rollo ${roll} -> ${success ? 'acerto' : 'penalidade'}`, () => {
      expect(isD20Success(roll)).toBe(success)
    })
  }
})
