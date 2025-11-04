import sys
import time

from git import Repo


def progress_bar_with_eta(
    iteration, total, prefix="", suffix="", length=30, fill="█", start_time=None
):
    if iteration == total:
        print()
        return

    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)

    # ETA calculation
    if start_time is not None:
        elapsed_time = time.time() - start_time
        estimated_total_time = elapsed_time / (iteration + 1) * total
        remaining_time = estimated_total_time - elapsed_time
        remaining_time_str = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
    else:
        remaining_time_str = "??:??:??"

    sys.stdout.write(
        f"\r{prefix} |{bar}| {percent}% {suffix} ETA: {remaining_time_str}"
    )
    sys.stdout.flush()


if __name__ == "__main__":
    start_time = time.time()

    repo = Repo(".")
    index = repo.index
    origin = repo.remote("origin")

    BRANCH = "main"
    MAX_COMMITS = 4_420_068
    PUSH_EVERY = 50_000

    for i in range(MAX_COMMITS):
        msg = f"Hello {'mom' if i % 2 == 0 else 'dad'}"
        index.commit(msg)

        # Update progress bar
        if i % 1_000 == 0:
            progress_bar_with_eta(
                i, MAX_COMMITS, suffix=f"{i:_}/{MAX_COMMITS:_}", start_time=start_time
            )

        # Push periodically
        if i % PUSH_EVERY == 0 and i != 0:
            try:
                origin.push(refspec=f"{BRANCH}:{BRANCH}")
                print(f"\n📤 Pushed {i:_} commits to origin/{BRANCH}")
            except Exception as e:
                print(f"\n⚠️ Push failed at {i:_}: {e}")

    # Final push
    origin.push(refspec=f"{BRANCH}:{BRANCH}")
    print(f"\n✅ All {MAX_COMMITS:_} commits pushed successfully.")
