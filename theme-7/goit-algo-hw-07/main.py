from sources.avl_tree_generator import generate_avl_tree
from sources.max_in_tree import find_max_in_tree
from sources.min_in_tree import find_min_in_tree
from sources.tree_sum import tree_sum
from sources.comments_tree import Comment


def main():
    while True:
        print("\n************ MENU ************")
        print("1. AVL Tree get maximum")
        print("2. AVL Tree get minimum")
        print("3. AVL Tree get sum of all nodes")
        print("4. Comments tree")
        print("0. Exit")
        print("******************************")
        choice = input("Select an option: ")

        if choice == '1':
            nodes_qty = input("Enter number of nodes for AVL tree: ")
            if not nodes_qty.isdigit() or int(nodes_qty) <= 0:
                print("Please enter a valid positive integer.")
                continue
            nodes_qty = int(nodes_qty)
            avl_tree_root, values_lst = generate_avl_tree(nodes_qty)
            max_value = find_max_in_tree(avl_tree_root)
            print(f"Generated AVL Tree with values: {values_lst}; max value: {max(values_lst)}")
            print(f"Maximum value in AVL Tree: {max_value}")

        elif choice == '2':
            nodes_qty = input("Enter number of nodes for AVL tree: ")
            if not nodes_qty.isdigit() or int(nodes_qty) <= 0:
                print("Please enter a valid positive integer.")
                continue
            nodes_qty = int(nodes_qty)
            avl_tree_root, values_lst = generate_avl_tree(nodes_qty)
            min_value = find_min_in_tree(avl_tree_root)
            print(f"Generated AVL Tree with values: {values_lst}; min value: {min(values_lst)}")
            print(f"Minimum value in AVL Tree: {min_value}")
        elif choice == '3':
            nodes_qty = input("Enter number of nodes for AVL tree: ")
            if not nodes_qty.isdigit() or int(nodes_qty) <= 0:
                print("Please enter a valid positive integer.")
                continue
            nodes_qty = int(nodes_qty)
            avl_tree_root, values_lst = generate_avl_tree(nodes_qty)
            total_sum = tree_sum(avl_tree_root)
            print(f"Generated AVL Tree with values: {values_lst}; sum of values: {sum(values_lst)}")
            print(f"Sum of all nodes in AVL Tree: {total_sum}")
        elif choice == '4':
            root_comment = Comment("This is the root comment.", "User1")
            reply1 = Comment("This is a reply to the root comment.", "User2")
            reply2 = Comment("This is another reply to the root comment.", "User3")
            sub_reply1 = Comment("This is a reply to the first reply.", "User4")

            root_comment.add_reply(reply1)
            root_comment.add_reply(reply2)
            reply1.add_reply(sub_reply1)

            print("Comments Tree Structure:")
            root_comment.display()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Please enter a valid option.")


if __name__ == "__main__":
    main()