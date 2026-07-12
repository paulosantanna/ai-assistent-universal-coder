import axios from 'axios';
import * as cheerio from 'cheerio';
import PQueue from 'p-queue';

interface ScrapeResult {
  url: string;
  title: string;
  content: string;
  links: string[];
  statusCode: number;
  error?: string;
  responseTimeMs: number;
}

interface BatchRequest {
  urls: string[];
  concurrency?: number;
  timeout?: number;
}

interface BatchResult {
  results: ScrapeResult[];
  totalTimeMs: number;
  succeeded: number;
  failed: number;
}

const DEFAULT_USER_AGENT = 'AEOS-ContinuousTraining-MCP/1.0 (TypeScript Scraper)';

function extractContent(html: string, url: string): ScrapeResult {
  const startTime = Date.now();
  const $ = cheerio.load(html);

  const title = $('title').first().text().trim();

  $('script, style, nav, footer, header, aside, noscript').remove();

  const content = $('body')
    .text()
    .replace(/\s+/g, ' ')
    .trim()
    .substring(0, 100000);

  const links: string[] = [];
  $('a[href]').each((_, el) => {
    const href = $(el).attr('href');
    if (href && href.startsWith('http')) {
      links.push(href);
    }
  });

  return {
    url,
    title,
    content,
    links: links.slice(0, 100),
    statusCode: 200,
    responseTimeMs: Date.now() - startTime,
  };
}

async function scrapeSingle(url: string, timeout: number = 30000): Promise<ScrapeResult> {
  const startTime = Date.now();
  try {
    const response = await axios.get(url, {
      timeout,
      headers: {
        'User-Agent': DEFAULT_USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
      },
      maxRedirects: 5,
      responseType: 'text',
    });

    const result = extractContent(response.data, url);
    result.statusCode = response.status;
    result.responseTimeMs = Date.now() - startTime;
    return result;
  } catch (error: any) {
    return {
      url,
      title: '',
      content: '',
      links: [],
      statusCode: error?.response?.status || 0,
      error: error?.message || 'Unknown error',
      responseTimeMs: Date.now() - startTime,
    };
  }
}

async function scrapeBatch(request: BatchRequest): Promise<BatchResult> {
  const startTime = Date.now();
  const concurrency = request.concurrency || 5;
  const timeout = request.timeout || 30000;

  const queue = new PQueue({ concurrency });
  const results: ScrapeResult[] = [];

  const tasks = request.urls.map((url) =>
    queue.add(async () => {
      const result = await scrapeSingle(url, timeout);
      return result;
    })
  );

  const settled = await Promise.allSettled(tasks);
  for (const result of settled) {
    if (result.status === 'fulfilled') {
      if (result.value) results.push(result.value);
    }
  }

  return {
    results,
    totalTimeMs: Date.now() - startTime,
    succeeded: results.filter((r) => !r.error).length,
    failed: results.filter((r) => r.error).length,
  };
}

async function main() {
  const input = process.argv[2];
  if (!input) {
    const chunks: string[] = [];
    for await (const chunk of process.stdin) {
      chunks.push(chunk.toString());
    }
    const inputData = chunks.join('');
    if (!inputData.trim()) {
      console.error(JSON.stringify({ error: 'No input provided' }));
      process.exit(1);
    }
    try {
      const request: BatchRequest = JSON.parse(inputData);
      const result = await scrapeBatch(request);
      console.log(JSON.stringify(result));
    } catch (e: any) {
      console.error(JSON.stringify({ error: e.message }));
      process.exit(1);
    }
  } else {
    try {
      const request: BatchRequest = JSON.parse(input);
      const result = await scrapeBatch(request);
      console.log(JSON.stringify(result));
    } catch (e: any) {
      console.error(JSON.stringify({ error: e.message }));
      process.exit(1);
    }
  }
}

main().catch((e) => {
  console.error(JSON.stringify({ error: e.message }));
  process.exit(1);
});
