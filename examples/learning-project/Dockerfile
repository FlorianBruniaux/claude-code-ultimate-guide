FROM node:22-alpine

WORKDIR /app

COPY package.json ./
COPY src ./src
COPY fixtures/release-ready.json ./fixtures/release-ready.json

USER node

ENTRYPOINT ["node", "src/cli.mjs"]
CMD ["verify", "fixtures/release-ready.json"]
