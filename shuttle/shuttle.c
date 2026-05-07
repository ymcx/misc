#define _XOPEN_SOURCE

#include <curl/curl.h>
#include <libxml/parser.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>

static const char *filename_gz = "file.gz";
static const char *filename_xml = "file.xml";
static const char *channels[] = {"YLE.TV1.fi", "YLE.TV2.fi", "MTV3.fi"};
static const char *url =
    "https://epgshare01.online/epgshare01/epg_ripper_FI1.xml.gz";

int matches_channel(const char *channel) {
  const size_t length = sizeof(channels) / sizeof(channels[0]);
  for (size_t i = 0; i < length; ++i) {
    if (strcmp(channel, channels[i]) == 0) {
      return 1;
    }
  }

  return 0;
}

size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
  return fwrite(ptr, size, nmemb, userdata);
}

void download_file(void) {
  // Create & truncate the output file
  FILE *file = fopen(filename_gz, "w");

  // Init
  curl_global_init(CURL_GLOBAL_NOTHING);
  CURL *curl = curl_easy_init();

  // Options
  curl_easy_setopt(curl, CURLOPT_URL, url);
  curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
  curl_easy_setopt(curl, CURLOPT_WRITEDATA, file);

  // Perform the action & do cleanup
  curl_easy_perform(curl);
  curl_easy_cleanup(curl);
  curl_global_cleanup();
  fclose(file);
}

void extract_file(void) {
  const gzFile file_in = gzopen64(filename_gz, "r");
  FILE *file_out = fopen(filename_xml, "w");

  char buf[8192];
  int bytes;

  while (1) {
    bytes = gzread(file_in, buf, 8192);
    if (bytes == 0) {
      break;
    }

    fwrite(buf, 1, bytes, file_out);
  }

  gzclose(file_in);
  fclose(file_out);
}

int parse_programme(const xmlNode *node, const int timezone_delta,
                    char *title_dst, char *start_dst, char *channel_dst) {
  const xmlChar *name = node->name;

  // The current node isn't a programme and we can exit early
  if (strcmp((const char *)name, "programme") != 0) {
    return 0;
  }

  xmlChar *channel = xmlGetProp(node, (const xmlChar *)"channel");

  // The channel of the current node is one that is not requested by the user
  if (!matches_channel((const char *)channel)) {
    xmlFree(channel);
    return 0;
  }

  // Parse the start time
  struct tm start_time;
  xmlChar *start = xmlGetProp(node, (const xmlChar *)"start");
  strptime((const char *)start, "%Y%m%d%H%M%S", &start_time);

  // Convert the start time to UNIX epoch and add our delta
  const time_t start_epoch = mktime(&start_time) + timezone_delta;

  // Convert back to a printable string
  char start_adjusted[32];
  struct tm *start_time_adjusted = localtime(&start_epoch);
  strftime(start_adjusted, sizeof(start_adjusted), "%d.%m.%Y %H:%M",
           start_time_adjusted);

  for (xmlNode *child = node->children; child; child = child->next) {
    const xmlChar *name = child->name;

    // We're only looking for the title. If the node is not a title object,
    // continue
    if (strcmp((const char *)name, "title") != 0) {
      continue;
    }

    xmlChar *title = xmlNodeGetContent(child);
    strcpy(title_dst, (const char *)title);
    xmlFree(title);

    break;
  }

  strcpy(channel_dst, (const char *)channel);
  strcpy(start_dst, start_adjusted);

  xmlFree(channel);
  xmlFree(start);

  return 1;
}

int get_timezone_delta(void) {
  struct tm time_local;
  struct tm time_utc;

  const time_t timer = time(NULL);
  localtime_r(&timer, &time_local);
  gmtime_r(&timer, &time_utc);

  const time_t epoch_local = mktime(&time_local);
  const time_t epoch_utc = mktime(&time_utc);

  return epoch_local - epoch_utc;
}

void parse_file(void) {
  const int timezone_delta = get_timezone_delta();

  char *start = malloc(1 * sizeof(char));
  char *title = malloc(1 * sizeof(char));
  char *channel = malloc(1 * sizeof(char));

  const xmlDoc *document = xmlReadFile(filename_xml, NULL, 0);
  const xmlNode *root = xmlDocGetRootElement(document);

  for (xmlNode *child = root->children; child; child = child->next) {
    // The current node either wasn't a programme or it's on the wrong channel
    if (!parse_programme(child, timezone_delta, title, start, channel)) {
      continue;
    }

    printf("%s - %s - %s\n", channel, start, title);
  }
}

int main(void) {
  download_file();
  extract_file();
  parse_file();
}
