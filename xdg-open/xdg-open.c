#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#include <fcntl.h>

#include <glib.h>
#include <gio/gio.h>
#include <gio/gunixfdlist.h>

int main(int argc, char **argv)
{
    if (argc != 2) {
        g_printerr("usage: xdg-open { file | URL }\n");
        return 1;
    }

    g_autoptr(GFile) file = g_file_new_for_commandline_arg(argv[1]);
    if (!file) {
        g_printerr("could not parse file name or URL\n");
        return 1;
    }

    g_autoptr(GError) error = NULL;
    g_autoptr(GDBusConnection) bus = g_bus_get_sync(
        G_BUS_TYPE_SESSION, NULL, &error);
    if (!bus) {
        g_printerr("could not connect to session bus: %s\n", error->message);
        return 1;
    }

    g_autoptr(GVariant) result = NULL;
    if (g_file_is_native(file)) {
        g_autofree char *path = g_file_get_path(file);

        int fd = open(path, O_RDONLY | O_CLOEXEC);
        if (fd == -1) {
            g_printerr("could not open file: %s\n", g_strerror(errno));
            return 1;
        }

        // fd_list takes ownership of the file descriptor
        g_autoptr(GUnixFDList) fd_list = g_unix_fd_list_new_from_array(&fd, 1);
        fd = -1;

        const char *parent_window = "";
        const int fd_index = 0;
        result = g_dbus_connection_call_with_unix_fd_list_sync(
            bus,
            "io.snapcraft.Launcher", "/io/snapcraft/Launcher",
            "io.snapcraft.Launcher", "OpenFile",
            g_variant_new("(sh)", parent_window, fd_index), NULL,
            G_DBUS_CALL_FLAGS_NONE, -1, fd_list, NULL, NULL, &error);
    } else {
        g_autofree char *uri = g_file_get_uri(file);

        result = g_dbus_connection_call_sync(
            bus,
            "io.snapcraft.Launcher", "/io/snapcraft/Launcher",
            "io.snapcraft.Launcher", "OpenURL",
            g_variant_new("(s)", uri), NULL,
            G_DBUS_CALL_FLAGS_NONE, -1, NULL, &error);
    }

    if (!result) {
        g_printerr("failed to launch: %s\n", error->message);
        return 1;
    }

    return 0;
}
