const message = "new Function(source)";
try {
  const parsed = JSON.parse(request.body);
} catch (error) {
  report(error);
}
const target = path.resolve(root, path.basename(requested));
fs.readFile(target, callback);
