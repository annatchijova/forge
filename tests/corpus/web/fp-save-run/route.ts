export function saveRun(input: string, body: string) {
  const slug = path.basename(input);
  const target = path.join("runs", slug);
  fs.writeFileSync(target, body);
}
