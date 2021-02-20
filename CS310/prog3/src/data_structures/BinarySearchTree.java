package data_structures;

import java.util.ConcurrentModificationException;
import java.util.Iterator;

/**
 * William Fox cssc0917
 * prog3 BinarySearchTree.java
 */
public class BinarySearchTree<K extends Comparable<K>, V> implements DictionaryADT<K, V> {
    private Node<K, V> root;
    private int size;
    private long modificationCounter;
    private K foundKey;

    public BinarySearchTree() {
        clear();
    }

    /**
     * Adds the given key/value pair to the dictionary.  Returns
     * false if the dictionary is full, or if the key is a duplicate.
     * Returns true if addition succeeded.
     *
     * @param key
     * @param value
     */
    public boolean add(K key, V value) {
        if (contains(key)) return false;
        Node<K, V> newNode = new Node<>(key, value);
        if (root == null)
            root = newNode;
        insert(key, value, root, null, false);
        size++;
        modificationCounter++;
        return true;

    }

    private void insert(K key, V value, Node<K, V> node, Node<K, V> parent, boolean wasLeft) {
        if (node == null) {
            if (wasLeft)
                parent.leftChild = new Node<>(key, value);
            else
                parent.rightChild = new Node<>(key, value);

        } else if (key.compareTo(node.key) < 0) //Go Left
            insert(key, value, node.leftChild, node, true);
        else if (key.compareTo(node.key) > 0)    //Go Right
            insert(key, value, node.rightChild, node, false);
    }

    /**
     * Deletes the key/value pair identified by the key parameter.
     * Returns true if the key/value pair was found and removed, otherwise false.
     *
     * @param key
     */
    public boolean delete(K key) {
        if (root == null) return false;
        if (!delete(key, root, null, false))
            return false;
        size--;
        modificationCounter++;
        return true;
    }

    //Navigates to node to remove
    private boolean delete(K key, Node<K, V> n, Node<K, V> parent, boolean wasLeft) {
        if (n == null) return false;
        if (key.compareTo(n.key) < 0)
            return delete(key, n.leftChild, n, true);
        else if (key.compareTo(n.key) > 0)
            return delete(key, n.rightChild, n, false);
        else //found
            if (n.leftChild == null && n.rightChild == null)//0 children
                if (wasLeft)
                    parent.leftChild = null;
                else
                    parent.rightChild = null;

            else if (n.leftChild == null)                //rightChild only
                if (wasLeft)
                    parent.leftChild = n.rightChild;
                else
                    parent.rightChild = n.rightChild;
            else if (n.rightChild == null)               //leftChild only
                if (wasLeft)
                    parent.leftChild = n.leftChild;
                else
                    parent.rightChild = n.leftChild;
            else {                                      //2 children'

                Node<K, V> uncle = n, cousin = n.rightChild; //Go right
                boolean wentLeft = false;
                while (cousin.leftChild != null) {    //Then left as possible
                    wentLeft = true;
                    uncle = cousin;
                    cousin = cousin.leftChild;
                }
                n.value = cousin.value;
                n.key = cousin.key;
                delete(n.key, cousin, uncle, wentLeft);
            }
        return true;
    }

    /**
     * Returns true if the dictionary has an object identified by
     * key in it, otherwise false.
     *
     * @param key
     */
    public boolean contains(K key) {
        return getValue(key) != null;
    }

    /**
     * Returns the value associated with the parameter key.  Returns
     * null if the key is not found or the dictionary is empty.
     *
     * @param key
     */
    public V getValue(K key) {
        return findValue(root, key);
    }

    private V findValue(Node<K, V> n, K key) {
        if (n == null)
            return null;
        int comp = n.key.compareTo(key);
        if (comp > 0) //Go Left
            return findValue(n.leftChild, key);
        else if (comp < 0) //Go Right
            return findValue(n.rightChild, key);
        else
            return n.value;
    }

    /**
     * Returns the key associated with the parameter value.  Returns
     * null if the value is not found in the dictionary.  If more
     * than one key exists that matches the given value, returns the
     * first one found.
     *
     * @param value
     */
    public K getKey(V value) {
        foundKey = null;
        findKey(root, value);
        return foundKey;
    }

    private void findKey(Node<K, V> node, V value) {
        if (node == null || foundKey != null)
            return;
        findKey(node.leftChild, value);
        if (((Comparable<V>) value).compareTo(node.value) == 0)
            foundKey = node.key;
        findKey(node.rightChild, value);
    }


    /**
     * Returns the number of key/value pairs currently stored
     * in the dictionary
     */
    public int size() {
        return size;
    }

    /**
     * Returns true if the dictionary is at max capacity
     */
    public boolean isFull() {
        return false;
    }

    /**
     * Returns true if the dictionary is empty
     */
    public boolean isEmpty() {
        return root == null;
    }

    /**
     * Returns the Dictionary object to an empty state.
     */
    public void clear() {
        root = null;
        modificationCounter = size = 0;
    }

    /**
     * Returns an Iterator of the keys in the dictionary, in ascending
     * sorted order.  The iterator must be fail-fast.
     */
    public Iterator<K> keys() {
        return new KeyIteratorHelper();
    }

    /**
     * Returns an Iterator of the values in the dictionary.  The
     * order of the values must match the order of the keys.
     * The iterator must be fail-fast.
     */
    public Iterator<V> values() {
        return new ValueIteratorHelper();
    }

    //~~~~~~~~~~~~~~~~~~~~~Iterators and DictionaryNode Classes Below~~~~~~~~~~~~~~~~~~~~~~~~

    abstract class IteratorHelper<E> implements Iterator<E> {
        protected Node<K, V>[] nodes;
        protected long modificationCheck;
        protected int index;

        public IteratorHelper() {
            nodes = new Node[size];
            index = 0;
            modificationCheck = modificationCounter;
            loadArray(root);
            index = 0; //index is used to load the array
        }

        protected void loadArray(Node<K, V> node) {
            if (node == null) return;
            loadArray(node.leftChild);
            nodes[index++] = node;
            loadArray(node.rightChild);
        }

        public boolean hasNext() {
            if (modificationCheck != modificationCounter)
                throw new ConcurrentModificationException();
            return index < size;
        }

        public abstract E next();

        public void remove() {
            throw new UnsupportedOperationException();
        }
    }// IteratorHelper

    class KeyIteratorHelper extends IteratorHelper<K> {

        public KeyIteratorHelper() {
            super();
        }

        public K next() {
            return nodes[index++].key;
        }
    }//KeyIteratorHelper

    class ValueIteratorHelper extends IteratorHelper<V> {
        public ValueIteratorHelper() {
            super();
        }

        public V next() {
            return nodes[index++].value;
        }
    }//ValueIteratorHelper

    private class Node<K extends Comparable<K>, V> implements Comparable<Node<K, V>> {
        K key;
        V value;
        Node<K, V> rightChild, leftChild;

        public Node(K k, V v) {
            key = k;
            value = v;
        }

        public int compareTo(Node<K, V> o) {
            return key.compareTo(o.key);
        }
    }//Node

}//Eof
