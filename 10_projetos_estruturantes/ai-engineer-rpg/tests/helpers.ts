// Utilitario de teste: um check falsificável para uso no PDF (sem importar engine extra).
export const blankPackLike = {
  test(s: string): boolean {
    return s.includes('___no-token-expected___')
  },
}
